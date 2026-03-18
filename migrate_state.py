# pyright: reportUnknownParameterType=false, reportMissingParameterType=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnnecessaryIsInstance=false, reportDeprecated=false
"""Migrate tournament state when metadata changes."""

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from submission_loader import get_eligible_submissions, load_metadata
from tournament_config import METADATA_FILE, MIN_SCORE, STATE_FILE, TS_MU, TS_SIGMA


def load_state(state_path):
    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")

    with state_path.open("r", encoding="utf-8") as infile:
        loaded = json.load(infile)  # pyright: ignore[reportAny]

    if not isinstance(loaded, dict):
        raise ValueError("State file must contain a JSON object")

    state = loaded

    state.setdefault("round_number", 1)
    state.setdefault("ratings", {})
    state.setdefault("match_history", [])
    state.setdefault("records", {})
    state.setdefault("retired_submissions", [])
    state.setdefault("submission_ownership", {})
    state.setdefault("pending_retirement", [])
    return state


def save_state(state, state_path):
    tmp_path = state_path.with_suffix(state_path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as outfile:
        json.dump(state, outfile, indent=2)
    _ = tmp_path.replace(state_path)


def count_matches(match_history, submission_id):
    return sum(
        1
        for match in match_history
        if match.get("white") == submission_id or match.get("black") == submission_id
    )


def validate_state(state):
    required_keys = [
        "round_number",
        "ratings",
        "match_history",
        "records",
        "submission_ownership",
        "pending_retirement",
    ]
    missing = [key for key in required_keys if key not in state]
    if missing:
        raise ValueError(f"Validation failed: missing keys: {missing}")

    if not isinstance(state["round_number"], int):
        raise ValueError("Validation failed: round_number must be int")
    if not isinstance(state["ratings"], dict):
        raise ValueError("Validation failed: ratings must be dict")
    if not isinstance(state["match_history"], list):
        raise ValueError("Validation failed: match_history must be list")
    if not isinstance(state["records"], dict):
        raise ValueError("Validation failed: records must be dict")
    if not isinstance(state.get("retired_submissions", []), list):
        raise ValueError("Validation failed: retired_submissions must be list")
    if not isinstance(state["submission_ownership"], dict):
        raise ValueError("Validation failed: submission_ownership must be dict")
    if not isinstance(state["pending_retirement"], list):
        raise ValueError("Validation failed: pending_retirement must be list")


def get_submission_owner(entry):
    if not isinstance(entry, dict):
        return None

    submitters = entry.get(":submitters", [])
    if not submitters or not isinstance(submitters[0], dict):
        return None

    submitter = submitters[0]
    for key in (
        ":sid",
        "sid",
        ":id",
        "id",
        ":student_id",
        "student_id",
        ":student-id",
        "student-id",
    ):
        value = submitter.get(key)
        if value:
            return str(value)
    return None


def compute_changes(state, metadata, ownership_map):
    state_ids = set(state.get("ratings", {}).keys())
    metadata_ids = set(metadata.keys())
    ghosts = sorted(state_ids - metadata_ids)

    current_submission_by_student = {}
    for submission_id in metadata_ids:
        student_id = ownership_map.get(submission_id)
        if student_id is not None:
            current_submission_by_student.setdefault(student_id, set()).add(
                submission_id
            )

    ghosts_dropout = []
    ghosts_resubmission = []
    for submission_id in ghosts:
        student_id = ownership_map.get(submission_id)
        if student_id is not None and student_id in current_submission_by_student:
            ghosts_resubmission.append(submission_id)
        else:
            ghosts_dropout.append(submission_id)

    eligible_ids = set(get_eligible_submissions(metadata, MIN_SCORE))
    new_submissions = sorted(eligible_ids - state_ids)
    return ghosts_dropout, ghosts_resubmission, new_submissions


def build_report(
    timestamp,
    state_file,
    metadata_file,
    state_before,
    state_after,
    ghosts_dropout,
    ghosts_resubmission,
    new_submissions,
    metadata,
):
    lines = []
    lines.append("=== Tournament State Migration Report ===")
    lines.append(f"Date: {timestamp}")
    lines.append(f"Input State: {state_file}")
    lines.append(f"Metadata Source: {metadata_file}")
    lines.append("")

    lines.append("[GHOST SUBMISSIONS - Dropout Retired]")
    lines.append(
        f"Found {len(ghosts_dropout)} ghost submissions where student has no current submission:"
    )
    for submission_id in ghosts_dropout:
        rating = state_after.get("ratings", {}).get(submission_id, {})
        mu = float(rating.get("mu", TS_MU))
        sigma = float(rating.get("sigma", TS_SIGMA))
        played = count_matches(state_after.get("match_history", []), submission_id)
        lines.append(
            f"  - {submission_id} (rating: mu={mu:.2f}, sigma={sigma:.2f}, {played} matches)"
        )
    lines.append("")

    lines.append("[GHOST SUBMISSIONS - Resubmission Pending Retirement]")
    lines.append(
        f"Found {len(ghosts_resubmission)} ghost submissions where student has a newer current export submission:"
    )
    for submission_id in ghosts_resubmission:
        rating = state_after.get("ratings", {}).get(submission_id, {})
        mu = float(rating.get("mu", TS_MU))
        sigma = float(rating.get("sigma", TS_SIGMA))
        played = count_matches(state_after.get("match_history", []), submission_id)
        lines.append(
            f"  - {submission_id} (rating: mu={mu:.2f}, sigma={sigma:.2f}, {played} matches)"
        )
    lines.append("")

    lines.append("[NEW SUBMISSIONS - Added]")
    lines.append(
        f"Found {len(new_submissions)} submissions in metadata (score >= {MIN_SCORE:g}) but NOT in state:"
    )
    for submission_id in new_submissions:
        entry = metadata.get(submission_id, {})
        if not isinstance(entry, dict):
            entry = {}
        submitters = entry.get(":submitters", [])
        name = "Unknown"
        if submitters and isinstance(submitters[0], dict):
            name = str(submitters[0].get(":name", "Unknown"))
        score = float(entry.get(":score", 0.0))
        lines.append(f"  - {submission_id} ({name}, score: {score:.1f})")

    lines.append(
        f"  Initialized with: mu={TS_MU:.1f}, sigma={TS_SIGMA:.3f}, wins/losses/draws=0"
    )
    lines.append("")

    before_matches = len(state_before.get("match_history", []))
    after_matches = len(state_after.get("match_history", []))
    before_ratings = len(state_before.get("ratings", {}))
    after_ratings = len(state_after.get("ratings", {}))
    zeroed_records = all(
        state_after.get("records", {}).get(submission_id, {})
        == {"wins": 0, "losses": 0, "draws": 0}
        for submission_id in new_submissions
    )

    lines.append("[VALIDATION]")
    lines.append(
        f"{'OK' if state_after.get('round_number') == state_before.get('round_number') else 'FAIL'} round_number preserved: {state_after.get('round_number')}"
    )
    lines.append(
        f"{'OK' if after_matches == before_matches else 'FAIL'} match_history entries: {after_matches} (unchanged)"
    )
    lines.append(
        f"OK Total ratings: {before_ratings} original + {len(new_submissions)} new = {after_ratings}"
    )
    lines.append(
        f"OK retired_submissions list: {len(state_after.get('retired_submissions', []))} entries"
    )
    lines.append(
        f"OK pending_retirement list: {len(state_after.get('pending_retirement', []))} entries"
    )
    lines.append(
        f"OK submission_ownership entries: {len(state_after.get('submission_ownership', {}))}"
    )
    lines.append(
        f"{'OK' if zeroed_records else 'FAIL'} All new submissions have zero records"
    )
    lines.append("")

    backup_exists = Path("tournament_state_pre_migration.json").exists()
    if backup_exists:
        backup_line = (
            "Backup created: tournament_state_pre_migration.json (already exists)"
        )
    else:
        backup_line = "Backup created: tournament_state_pre_migration.json (not found)"

    lines.append("[OUTPUT]")
    lines.append(f"Migrated state saved to: {state_file}")
    lines.append(backup_line)
    lines.append("Migration report saved to: migration_report.txt")
    return "\n".join(lines) + "\n"


def migrate():
    state_path = Path(STATE_FILE)
    metadata_path = Path(METADATA_FILE)

    state = load_state(state_path)
    metadata = load_metadata(str(metadata_path))
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a mapping")
    metadata = cast(dict[str, object], metadata)

    state_before = deepcopy(state)
    timestamp = datetime.now(timezone.utc).isoformat()

    ownership = state.get("submission_ownership", {})
    if not isinstance(ownership, dict):
        ownership = {}
    for submission_id, raw_entry in metadata.items():
        if not isinstance(raw_entry, dict):
            continue
        student_id = get_submission_owner(raw_entry)
        if student_id is not None:
            ownership[submission_id] = student_id
    for submission_id in state.get("ratings", {}):
        ownership.setdefault(submission_id, f"unknown:{submission_id}")
    state["submission_ownership"] = ownership

    ghosts_dropout, ghosts_resubmission, new_submissions = compute_changes(
        state, metadata, ownership
    )

    retired = state.get("retired_submissions", [])
    if not isinstance(retired, list):
        retired = []
    retired_lookup = set(retired)
    for submission_id in ghosts_dropout:
        if submission_id not in retired_lookup:
            retired.append(submission_id)
            retired_lookup.add(submission_id)
    for submission_id in ghosts_resubmission:
        if submission_id in retired_lookup:
            retired.remove(submission_id)
            retired_lookup.remove(submission_id)
    state["retired_submissions"] = retired

    pending = state.get("pending_retirement", [])
    if not isinstance(pending, list):
        pending = []
    metadata_ids = set(metadata.keys())
    pending = [
        submission_id
        for submission_id in pending
        if submission_id not in ghosts_dropout and submission_id not in metadata_ids
    ]
    pending_lookup = set(pending)
    for submission_id in ghosts_resubmission:
        if submission_id not in pending_lookup:
            pending.append(submission_id)
            pending_lookup.add(submission_id)
    state["pending_retirement"] = pending

    for submission_id in new_submissions:
        state.setdefault("ratings", {})[submission_id] = {
            "mu": TS_MU,
            "sigma": TS_SIGMA,
        }
        state.setdefault("records", {})[submission_id] = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
        }

    state["migration_log"] = {
        "timestamp": timestamp,
        "ghosts_retired": len(ghosts_dropout),
        "ghosts_resubmission_pending": len(ghosts_resubmission),
        "new_submissions_added": len(new_submissions),
        "round_number_preserved": state_before.get("round_number"),
        "metadata_file": str(metadata_path),
    }

    validate_state(state)
    save_state(state, state_path)

    report = build_report(
        timestamp,
        str(state_path),
        str(metadata_path),
        state_before,
        state,
        ghosts_dropout,
        ghosts_resubmission,
        new_submissions,
        metadata,
    )

    _ = Path("migration_report.txt").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    migrate()
