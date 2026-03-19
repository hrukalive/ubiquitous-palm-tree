import argparse
import glob
import hashlib
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

from trueskill import Rating

from submission_loader import (
    build_submission_catalog,
    load_all_metadata,
    load_profile_name,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    import tournament_config

    return tournament_config


def initialize_state() -> Dict[str, Any]:
    return {"round_number": 1, "ratings": {}, "match_history": [], "records": {}}


def load_state(state_file: str) -> Dict[str, Any]:
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("round_number", 1)
                    data.setdefault("ratings", {})
                    data.setdefault("match_history", [])
                    data.setdefault("records", {})
                    return data
        except Exception:
            pass
    return initialize_state()


def find_match_results(
    round_num: int, results_dir: str = "results"
) -> List[Dict[str, Any]]:
    round_dir = os.path.join(results_dir, f"round_{round_num:02d}")
    if not os.path.exists(round_dir):
        return []
    all_matches: List[Dict[str, Any]] = []
    matches_file = os.path.join(round_dir, "matches.json")
    if os.path.exists(matches_file):
        try:
            with open(matches_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_matches.extend(data)
        except Exception:
            pass
    for match_file in glob.glob(os.path.join(round_dir, "*match_*.json")):
        try:
            with open(match_file, "r", encoding="utf-8") as f:
                match_data = json.load(f)
                if isinstance(match_data, dict):
                    all_matches.append(match_data)
        except Exception:
            pass
    return all_matches


def rating_to_dict(rating: Rating) -> Dict[str, float]:
    return {"mu": rating.mu, "sigma": rating.sigma}


def dict_to_rating(data: Dict[str, float]) -> Rating:
    return Rating(mu=data.get("mu", 25.0), sigma=data.get("sigma", 8.333))


def compute_conservative_rating(mu: float, sigma: float) -> float:
    return mu - 3 * sigma


def compute_main_score_bucket(
    mu: float, sigma: float, precision: int
) -> float:
    return round(compute_conservative_rating(mu, sigma), precision)


def build_tiebreak_fingerprint(state: Dict[str, Any], precision: int) -> str:
    ratings = state.get("ratings", {})
    normalized = []
    for submission_id in sorted(ratings):
        rating = ratings.get(submission_id, {})
        mu = float(rating.get("mu", 25.0))
        sigma = float(rating.get("sigma", 8.333))
        normalized.append(
            {
                "submission_id": submission_id,
                "mu": round(mu, precision),
                "sigma": round(sigma, precision),
                "main_score_bucket": compute_main_score_bucket(
                    mu, sigma, precision
                ),
            }
        )
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def collect_results(round_num: int, state_file: str = "tournament_state.json"):
    config = load_config()
    state = load_state(state_file)
    matches = find_match_results(round_num, config.RESULTS_DIR)
    logger.info("Round %s: Found %s match result files", round_num, len(matches))
    if not matches:
        return state

    processed = {
        (m.get("match_id"), m.get("round")) for m in state.get("match_history", [])
    }
    ts_env: Any = config.trueskill_env
    processed_count = 0
    skipped_count = 0

    for match in matches:
        match_id = match.get("match_id")
        white_sub = match.get("white_submission") or match.get("white")
        black_sub = match.get("black_submission") or match.get("black")
        winner = match.get("winner")

        if (match_id, round_num) in processed or not white_sub or not black_sub:
            skipped_count += 1
            continue

        processed_count += 1
        for sub in [white_sub, black_sub]:
            state["ratings"].setdefault(
                sub, {"mu": config.TS_MU, "sigma": config.TS_SIGMA}
            )
            state["records"].setdefault(
                sub, {"wins": 0, "losses": 0, "draws": 0}
            )

        wr = dict_to_rating(state["ratings"][white_sub])
        br = dict_to_rating(state["ratings"][black_sub])

        if winner == "white":
            nw, nb = ts_env.rate_1vs1(wr, br)
            state["records"][white_sub]["wins"] += 1
            state["records"][black_sub]["losses"] += 1
        elif winner == "black":
            nb, nw = ts_env.rate_1vs1(br, wr)
            state["records"][black_sub]["wins"] += 1
            state["records"][white_sub]["losses"] += 1
        elif winner is None or winner == "draw":
            nw, nb = ts_env.rate_1vs1(wr, br, drawn=True)
            state["records"][white_sub]["draws"] += 1
            state["records"][black_sub]["draws"] += 1
        else:
            continue

        state["ratings"][white_sub] = rating_to_dict(nw)
        state["ratings"][black_sub] = rating_to_dict(nb)
        state["match_history"].append(
            {
                "match_id": match_id,
                "white": white_sub,
                "black": black_sub,
                "winner": winner,
                "round": round_num,
            }
        )

    logger.info(
        "Round %s: Processed %s new matches, skipped %s",
        round_num,
        processed_count,
        skipped_count,
    )
    state["round_number"] = round_num + 1
    return state


def save_state(state: Dict[str, Any], state_file: str) -> bool:
    try:
        tmp_file = state_file + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp_file, state_file)
        return True
    except Exception:
        return False


def load_submission_details() -> Dict[str, Dict[str, str]]:
    config = load_config()
    metadata = load_all_metadata(config.SUBMISSIONS_DIR)
    catalog = build_submission_catalog(config.SUBMISSIONS_DIR)
    details: Dict[str, Dict[str, str]] = {}

    for submission_id, data in metadata.items():
        if not isinstance(data, dict):
            continue
        submitters = data.get(":submitters", [{}])
        submitter = submitters[0] if submitters else {}
        email = submitter.get(":email", "") if isinstance(submitter, dict) else ""
        entry = catalog.get(submission_id, {})
        submission_dir = entry.get("submission_dir", "")
        profile = (
            load_profile_name(submission_dir)
            if isinstance(submission_dir, str) and submission_dir
            else None
        )
        name = submitter.get(":name", "Unknown") if isinstance(submitter, dict) else "Unknown"
        details[submission_id] = {
            "name": str(name),
            "username": email.split("@")[0] if email else "",
            "profile": profile or str(name),
            "student_id": str(submitter.get(":sid", "")) if isinstance(submitter, dict) else "",
        }

    return details


def load_tiebreak_results_for_state(state: Dict[str, Any]) -> Dict[str, Any]:
    config = load_config()
    tiebreak_file = config.TIEBREAK_FILE
    if not os.path.exists(tiebreak_file):
        return {}

    try:
        with open(tiebreak_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except Exception as exc:
        logger.warning("Failed to load tiebreak results from %s: %s", tiebreak_file, exc)
        return {}

    if not isinstance(loaded, dict):
        return {}

    precision = int(loaded.get("score_precision", config.TIEBREAK_SCORE_PRECISION))
    expected_fingerprint = build_tiebreak_fingerprint(state, precision)
    if loaded.get("state_fingerprint") != expected_fingerprint:
        logger.info("Ignoring stale tiebreak results in %s", tiebreak_file)
        return {}

    return loaded


def generate_leaderboard(
    state: Dict[str, Any],
    tiebreak_results: Optional[Dict[str, Any]] = None,
) -> str:
    config = load_config()
    details = load_submission_details()
    precision = config.TIEBREAK_SCORE_PRECISION
    resolved_tiebreak_results = (
        tiebreak_results
        if isinstance(tiebreak_results, dict)
        else load_tiebreak_results_for_state(state)
    )
    tiebreak_rankings = {}
    if isinstance(resolved_tiebreak_results, dict):
        rankings = resolved_tiebreak_results.get("rankings", {})
        if isinstance(rankings, dict):
            tiebreak_rankings = rankings

    data = []
    for submission_id, rating in state.get("ratings", {}).items():
        mu = float(rating.get("mu", config.TS_MU))
        sigma = float(rating.get("sigma", config.TS_SIGMA))
        main_score = compute_conservative_rating(mu, sigma)
        main_score_bucket = compute_main_score_bucket(mu, sigma, precision)
        record = state.get("records", {}).get(
            submission_id, {"wins": 0, "losses": 0, "draws": 0}
        )
        detail = details.get(
            submission_id,
            {
                "name": "Unknown",
                "username": "",
                "profile": "Unknown",
                "student_id": "",
            },
        )
        tb_entry = tiebreak_rankings.get(submission_id, {})
        tiebreak_main_score = tb_entry.get("main_score")
        tiebreak_score = (
            tb_entry.get("score")
            if isinstance(tiebreak_main_score, (int, float))
            and round(float(tiebreak_main_score), precision) == main_score_bucket
            else None
        )
        tiebreak_rank = (
            int(tb_entry.get("rank"))
            if tiebreak_score is not None and isinstance(tb_entry.get("rank"), int)
            else None
        )
        data.append(
            {
                "sid": submission_id,
                "student_id": detail["student_id"],
                "name": detail["name"],
                "username": detail["username"],
                "profile": detail["profile"],
                "mu": mu,
                "sigma": sigma,
                "main_score": main_score,
                "main_score_bucket": main_score_bucket,
                "tiebreak_score": float(tiebreak_score)
                if isinstance(tiebreak_score, (int, float))
                else None,
                "tiebreak_rank": tiebreak_rank,
                "w": int(record.get("wins", 0)),
                "l": int(record.get("losses", 0)),
                "d": int(record.get("draws", 0)),
            }
        )

    data.sort(
        key=lambda item: (
            -item["main_score_bucket"],
            item["tiebreak_rank"] if item["tiebreak_rank"] is not None else float("inf"),
            -item["tiebreak_score"] if item["tiebreak_score"] is not None else float("inf"),
            -item["main_score"],
            -item["mu"],
            str(item["sid"]),
        )
    )

    deduped = []
    seen_students = set()
    for entry in data:
        student_key = entry["student_id"] or entry["sid"]
        if student_key in seen_students:
            continue
        seen_students.add(student_key)
        deduped.append(entry)

    header = (
        f"{'Rank':>4} | {'Name':20} | {'Username':15} | {'Profile':30} | "
        f"{'Submission ID':20} | {'Main':>8} | {'TB':>8} | {'Rating (mu+/-sigma)':16} | {'Record'}"
    )
    divider = "=" * len(header)
    lines = [
        divider,
        "BREAKTHROUGH LEADERBOARD",
        divider,
        "",
        header,
        "-" * len(header),
    ]

    for rank, entry in enumerate(deduped, 1):
        tb_display = (
            f"{entry['tiebreak_score']:.2f}"
            if entry["tiebreak_score"] is not None
            else "-"
        )
        lines.append(
            f"{rank:4} | {entry['name'][:20]:20} | {entry['username'][:15]:15} | "
            f"{entry['profile'][:30]:30} | {entry['sid'][:20]:20} | "
            f"{entry['main_score']:8.2f} | {tb_display:>8} | "
            f"{entry['mu']:9.2f}+/-{entry['sigma']:6.2f} | {entry['w']}-{entry['l']}-{entry['d']}"
        )

    lines.append(divider)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", "-r", type=int, required=True)
    parser.add_argument("--state", type=str, default="tournament_state.json")
    parser.add_argument("--leaderboard", type=str, default="leaderboard.txt")
    args = parser.parse_args()
    state = collect_results(args.round, args.state)
    if not save_state(state, args.state):
        sys.exit(1)
    with open(args.leaderboard, "w", encoding="utf-8") as f:
        f.write(generate_leaderboard(state))


if __name__ == "__main__":
    main()
