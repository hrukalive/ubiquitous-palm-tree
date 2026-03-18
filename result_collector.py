import json, os, sys, logging, argparse, glob, copy
from typing import Dict, Any, List, Optional, Tuple
from trueskill import Rating

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
            with open(state_file, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                return initialize_state()
        except:
            return initialize_state()
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
            with open(matches_file, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_matches.extend(data)
        except:
            pass
    for match_file in glob.glob(os.path.join(round_dir, "*match_*.json")):
        try:
            with open(match_file, "r") as f:
                match_data = json.load(f)
                if isinstance(match_data, dict):
                    all_matches.append(match_data)
        except:
            pass
    return all_matches


def rating_to_dict(rating):
    return {"mu": rating.mu, "sigma": rating.sigma}


def dict_to_rating(data):
    return Rating(mu=data.get("mu", 25.0), sigma=data.get("sigma", 8.333))


def collect_results(round_num: int, state_file: str = "tournament_state.json"):
    config = load_config()
    state = load_state(state_file)
    matches = find_match_results(round_num)
    logger.info(f"Round {round_num}: Found {len(matches)} match result files")
    if not matches:
        return state
    processed = {
        (m.get("match_id"), m.get("round")) for m in state.get("match_history", [])
    }
    logger.info(f"Round {round_num}: {len(processed)} matches already in history")
    ts_env: Any = config.trueskill_env
    if "records" not in state:
        state["records"] = {}
    processed_count = 0
    skipped_count = 0
    for match in matches:
        match_id, white_sub, black_sub, winner = (
            match.get("match_id"),
            match.get("white_submission") or match.get("white"),
            match.get("black_submission") or match.get("black"),
            match.get("winner"),
        )
        if (match_id, round_num) in processed or not white_sub or not black_sub:
            skipped_count += 1
            continue
        processed_count += 1
        for sub in [white_sub, black_sub]:
            if sub not in state["ratings"]:
                state["ratings"][sub] = {"mu": config.TS_MU, "sigma": config.TS_SIGMA}
            if sub not in state["records"]:
                state["records"][sub] = {"wins": 0, "losses": 0, "draws": 0}
        wr, br = (
            dict_to_rating(state["ratings"][white_sub]),
            dict_to_rating(state["ratings"][black_sub]),
        )
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
        state["ratings"][white_sub], state["ratings"][black_sub] = (
            rating_to_dict(nw),
            rating_to_dict(nb),
        )
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
        f"Round {round_num}: Processed {processed_count} new matches, skipped {skipped_count}"
    )
    state["round_number"] = round_num + 1
    return state


def _compute_tier_constraints(
    tied_groups: List[List[str]],
    snapshot_ratings: Dict[str, Dict[str, float]],
    precision: int = 2,
) -> Dict[int, Dict[str, Any]]:
    """
    Compute tier boundary constraints for each tied group.

    Args:
        tied_groups: List of tied player groups, e.g., [["p1", "p2", "p3"], ["p4", "p5"]]
        snapshot_ratings: Snapshot of ratings at tiebreaker start {player_id: {"mu", "sigma"}}
        precision: Decimal places for rounding (for tier detection)

    Returns:
        Dict mapping group_idx -> {"players", "orig", "isolated", "mu_floor", "mu_ceiling", ...}
    """
    group_ctx = {}

    for group_idx, group in enumerate(tied_groups):
        # Capture original ratings for this group
        orig_ratings = {p: copy.deepcopy(snapshot_ratings[p]) for p in group}

        # Compute tier bounds (min/max mu in this group)
        mus = [orig_ratings[p]["mu"] for p in group]
        mu_floor = min(mus) if mus else 25.0
        mu_ceiling = max(mus) if mus else 25.0

        # Initialize isolated pool with original ratings
        isolated = {
            p: {"mu": orig_ratings[p]["mu"], "sigma": orig_ratings[p]["sigma"]}
            for p in group
        }

        # Frozen conservative score from original tier state (no rounding)
        frozen_cons = {
            p: orig_ratings[p]["mu"] - 3 * orig_ratings[p]["sigma"] for p in group
        }

        group_ctx[group_idx] = {
            "players": group,
            "orig": orig_ratings,
            "isolated": isolated,
            "frozen_cons": frozen_cons,
            "mu_floor": mu_floor,
            "mu_ceiling": mu_ceiling,
            "processed_matches": 0,
        }

    return group_ctx


def _apply_isolated_match_update(
    isolated_ratings: Dict[str, Dict[str, float]],
    white: str,
    black: str,
    winner: Optional[str],
    ts_env,
) -> None:
    """
    Apply TrueSkill update to isolated rating pool (modifies in-place).

    Args:
        isolated_ratings: Dict of {player_id: {"mu", "sigma"}} for isolated pool
        white: White player ID
        black: Black player ID
        winner: "white", "black", or None/"draw"
        ts_env: TrueSkill environment from tournament_config
    """
    # Get ratings from isolated pool
    wr = Rating(
        mu=isolated_ratings[white]["mu"], sigma=isolated_ratings[white]["sigma"]
    )
    br = Rating(
        mu=isolated_ratings[black]["mu"], sigma=isolated_ratings[black]["sigma"]
    )

    # Apply TrueSkill update
    if winner == "white":
        nw, nb = ts_env.rate_1vs1(wr, br)
    elif winner == "black":
        nb, nw = ts_env.rate_1vs1(br, wr)
    elif winner is None or winner == "draw":
        nw, nb = ts_env.rate_1vs1(wr, br, drawn=True)
    else:
        return  # Invalid winner

    # Write back to isolated pool
    isolated_ratings[white] = {"mu": nw.mu, "sigma": nw.sigma}
    isolated_ratings[black] = {"mu": nb.mu, "sigma": nb.sigma}


def _project_group_back_to_tier(
    group_ctx: Dict[str, Any],
    precision: int = 2,
) -> Dict[str, Dict[str, float]]:
    """
    Project isolated pool ratings back to tier-constrained mu values.

    Ranks players by isolated mu (desc), then interpolates mu within tier bounds.
    Ensures no player crosses tier boundaries.

    Args:
        group_ctx: Context dict with "players", "orig", "isolated", "mu_floor", "mu_ceiling"
        precision: Decimal places for rounding

    Returns:
        Dict of {player_id: {"mu", "sigma"}} with tier-constrained mu values
    """
    players = group_ctx["players"]
    isolated = group_ctx["isolated"]
    frozen_cons = group_ctx["frozen_cons"]
    mu_floor = group_ctx["mu_floor"]
    mu_ceiling = group_ctx["mu_ceiling"]

    # Rank players by frozen conservative score, then isolated conservative score
    ranked_players = sorted(
        players,
        key=lambda p: (
            -frozen_cons[p],  # Primary: higher frozen conservative is better
            -(
                isolated[p]["mu"] - 3 * isolated[p]["sigma"]
            ),  # Secondary: new conservative
            isolated[p]["sigma"],  # Tertiary: lower sigma is better
            p,  # Quaternary: player ID for determinism
        ),
    )

    # Compute interpolation range
    tier_range = mu_ceiling - mu_floor

    # If tier_range is zero or too small, use micro-spacing
    if tier_range < 0.01 and len(ranked_players) > 1:
        tier_range = 0.5
        mu_floor = mu_ceiling - tier_range

    # Interpolate mu values
    result = {}
    for rank_idx, player in enumerate(ranked_players):
        if len(ranked_players) == 1:
            # Single player: keep at ceiling
            new_mu = mu_ceiling
        else:
            # Interpolate: rank 0 -> ceiling, rank n-1 -> floor
            normalized_rank = rank_idx / (len(ranked_players) - 1)
            new_mu = mu_ceiling - (normalized_rank * tier_range)

        # Round to precision
        new_mu = round(new_mu, precision)

        # Clamp to tier bounds to be safe
        new_mu = max(mu_floor, min(mu_ceiling, new_mu))

        # Use sigma from isolated pool (reflects matches)
        new_sigma = isolated[player]["sigma"]

        result[player] = {"mu": new_mu, "sigma": new_sigma}

    # Validate frozen conservative ordering invariant
    for i in range(len(ranked_players) - 1):
        assert frozen_cons[ranked_players[i]] >= frozen_cons[ranked_players[i + 1]]

    # Validate projected mu bounds
    for player in ranked_players:
        new_mu = result[player]["mu"]
        assert mu_floor <= new_mu <= mu_ceiling

    return result


def collect_tiebreaker_results(
    round_num: int,
    state: Dict[str, Any],
    results_dir: str = "results",
    tied_groups: Optional[List[List[str]]] = None,
    precision: int = 2,
    enforce_tier_isolation: bool = False,
) -> Dict[str, Any]:
    """
    Collect and process tiebreaker match results with optional tier-preserving isolation.

    Tier-Preserving Tiebreaker (enforce_tier_isolation=True):
    - Matches run in isolated TrueSkill namespace per tied group
    - After matches, ratings projected back to tier bounds [mu_floor, mu_ceiling]
    - No player can end with mu outside their group's original range
    - Example: top 3 tied group (μ∈[35.0, 35.81]) stays within bounds after tiebreaker

    Legacy Behavior (enforce_tier_isolation=False or tied_groups=None):
    - Direct TrueSkill updates on global state (original behavior)
    - Allows players to cross tier boundaries

    CRITICAL: Unlike collect_results(), this function does NOT modify state['round_number'].
    This preserves the main tournament round counter while allowing tiebreaker rounds (100+)
    to update ratings and records without interfering with the main tournament flow.

    Args:
        round_num: Tiebreaker round number (100+)
        state: Tournament state dict (modified in-place)
        results_dir: Results directory base path (default: 'results')
        tied_groups: Optional list of tied player groups for tier isolation
        precision: Decimal places for rounding (default: 2)
        enforce_tier_isolation: If True and tied_groups provided, use tier-preserving logic

    Returns:
        Updated state dict (same object, modified in-place)
    """
    config = load_config()
    ts_env: Any = config.trueskill_env

    # Fallback to legacy if tier isolation not requested or tied_groups not provided
    if not enforce_tier_isolation or not tied_groups:
        return _collect_tiebreaker_results_legacy(round_num, state, results_dir)

    # Find match result files for this tiebreaker round
    matches = find_match_results(round_num, results_dir)

    if not matches:
        logger.warning(f"No tiebreaker matches found for round {round_num}")
        return state

    # Snapshot ratings before processing (for tier constraint computation)
    snapshot_ratings = copy.deepcopy(state["ratings"])

    # Compute tier constraints and initialize isolated pools
    group_ctx = _compute_tier_constraints(tied_groups, snapshot_ratings, precision)

    # Track processed matches to avoid duplicates
    processed = set((m["match_id"], m["round"]) for m in state.get("match_history", []))
    processed_count = 0
    skipped_count = 0

    # Process each match result in isolated pools
    for match in matches:
        match_id = match.get("match_id")
        white_sub = match.get("white_submission") or match.get("white")
        black_sub = match.get("black_submission") or match.get("black")
        winner = match.get("winner")

        # Skip if already processed or invalid (bye matches have no winner)
        if (
            (match_id, round_num) in processed
            or not white_sub
            or not black_sub
            or "winner" not in match
        ):
            skipped_count += 1
            continue

        # Find which group these players belong to
        group_idx = None
        for gidx, ctx in group_ctx.items():
            if white_sub in ctx["players"] and black_sub in ctx["players"]:
                group_idx = gidx
                break

        if group_idx is None:
            # Players not in tied groups; skip tier isolation for this match
            skipped_count += 1
            continue

        processed_count += 1
        ctx = group_ctx[group_idx]

        # Apply isolated match update
        _apply_isolated_match_update(
            ctx["isolated"], white_sub, black_sub, winner, ts_env
        )
        ctx["processed_matches"] += 1

        # Initialize records if needed
        for sub in [white_sub, black_sub]:
            if sub not in state["records"]:
                state["records"][sub] = {"wins": 0, "losses": 0, "draws": 0}

        # Update records (track W-L-D for stats, but don't touch global ratings yet)
        if winner == "white":
            state["records"][white_sub]["wins"] += 1
            state["records"][black_sub]["losses"] += 1
        elif winner == "black":
            state["records"][black_sub]["wins"] += 1
            state["records"][white_sub]["losses"] += 1
        elif winner is None or winner == "draw":
            state["records"][white_sub]["draws"] += 1
            state["records"][black_sub]["draws"] += 1

        # Add to match history (will need ratings later)
        state["match_history"].append(
            {
                "match_id": match_id,
                "white": white_sub,
                "black": black_sub,
                "winner": winner,
                "round": round_num,
            }
        )

    # Project isolated ratings back to tier-constrained values
    for group_idx, ctx in group_ctx.items():
        if ctx["processed_matches"] == 0:
            continue  # No matches processed in this group

        projected_ratings = _project_group_back_to_tier(ctx, precision)

        # Update global state with tier-constrained ratings
        for player, rating in projected_ratings.items():
            state["ratings"][player] = rating

    logger.info(
        f"Tiebreaker round {round_num}: Processed {processed_count} matches, skipped {skipped_count}"
    )

    # CRITICAL: Do NOT modify state['round_number']
    # This preserves the main tournament round counter

    return state


def _collect_tiebreaker_results_legacy(
    round_num: int, state: Dict[str, Any], results_dir: str = "results"
) -> Dict[str, Any]:
    """
    Legacy tiebreaker result collection (original implementation).

    Applies TrueSkill updates directly to global state without tier isolation.
    Used when enforce_tier_isolation=False or tied_groups not provided.

    Args:
        round_num: Tiebreaker round number (100+)
        state: Tournament state dict (modified in-place)
        results_dir: Results directory base path (default: 'results')

    Returns:
        Updated state dict (same object, modified in-place)
    """
    config = load_config()
    ts_env: Any = config.trueskill_env

    # Find match result files for this tiebreaker round
    matches = find_match_results(round_num, results_dir)

    if not matches:
        logger.warning(f"No tiebreaker matches found for round {round_num}")
        return state

    # Track processed matches to avoid duplicates
    processed = set((m["match_id"], m["round"]) for m in state.get("match_history", []))
    processed_count = 0
    skipped_count = 0

    # Process each match result
    for match in matches:
        match_id = match.get("match_id")
        white_sub = match.get("white_submission") or match.get("white")
        black_sub = match.get("black_submission") or match.get("black")
        winner = match.get("winner")

        # Skip if already processed or invalid (bye matches have no winner)
        if (
            (match_id, round_num) in processed
            or not white_sub
            or not black_sub
            or "winner" not in match
        ):
            skipped_count += 1
            continue

        processed_count += 1

        # Initialize ratings and records if needed
        for sub in [white_sub, black_sub]:
            if sub not in state["ratings"]:
                state["ratings"][sub] = {"mu": config.TS_MU, "sigma": config.TS_SIGMA}
            if sub not in state["records"]:
                state["records"][sub] = {"wins": 0, "losses": 0, "draws": 0}

        # Get current ratings
        wr = dict_to_rating(state["ratings"][white_sub])
        br = dict_to_rating(state["ratings"][black_sub])

        # Update ratings based on outcome
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
            continue  # Invalid winner value

        # Save updated ratings
        state["ratings"][white_sub] = rating_to_dict(nw)
        state["ratings"][black_sub] = rating_to_dict(nb)

        # Add to match history
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
        f"Tiebreaker round {round_num}: Processed {processed_count} matches, skipped {skipped_count}"
    )

    # CRITICAL: Do NOT modify state['round_number']
    # This preserves the main tournament round counter

    return state


def save_state(state, state_file):
    try:
        tmp_file = state_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp_file, state_file)
        return True
    except:
        return False


def check_and_retire_lower_ranked(state):
    """
    Compare same-student submissions and retire lower-ranked ones.

    For each student with 2+ active (non-retired) submissions:
    - Compare by (frozen_cons, cons, submission_id) tuple
    - Keep highest-ranked submission active
    - Move all lower-ranked to retired_submissions
    - Remove retired ones from pending_retirement

    Returns: modified state dict
    """
    config = load_config()

    ownership = state.get("submission_ownership", {})
    if not isinstance(ownership, dict):
        ownership = {}

    ratings = state.get("ratings", {})
    if not isinstance(ratings, dict):
        ratings = {}

    frozen_scores = state.get("frozen_conservative", {})
    if not isinstance(frozen_scores, dict):
        frozen_scores = {}

    pending = list(state.get("pending_retirement", []))
    retired = set(state.get("retired_submissions", []))

    # Group ALL active (non-retired) submissions by student ownership.
    # This includes both pending submissions AND current active submissions.
    student_submissions = {}
    for sub_id in ratings.keys():
        if sub_id in retired:
            continue  # Skip already-retired submissions
        student_id = ownership.get(sub_id)
        if not student_id:
            continue
        student_submissions.setdefault(student_id, []).append(sub_id)

    retired_now = set()

    for student_id, sub_ids in student_submissions.items():
        if len(sub_ids) < 2:
            continue

        def _ranking_score(sid):
            rating = ratings.get(sid, {})
            mu = rating.get("mu", config.TS_MU)
            sigma = rating.get("sigma", config.TS_SIGMA)
            current_cons = mu - 3 * sigma
            frozen_cons = frozen_scores.get(sid, current_cons)
            return frozen_cons, current_cons

        ranked = sorted(
            sub_ids,
            key=lambda sid: (_ranking_score(sid)[0], _ranking_score(sid)[1], str(sid)),
            reverse=True,
        )

        keep_sid = ranked[0]
        lower_ranked = ranked[1:]

        for retire_sid in lower_ranked:
            if retire_sid not in retired:
                retired.add(retire_sid)
            retired_now.add(retire_sid)
            logger.info(
                "Retiring lower-ranked submission for student %s: kept %s score=%s, retired %s score=%s",
                student_id,
                keep_sid,
                _ranking_score(keep_sid),
                retire_sid,
                _ranking_score(retire_sid),
            )

    if retired_now:
        pending = [sub_id for sub_id in pending if sub_id not in retired_now]

    state["pending_retirement"] = sorted(pending, key=str)
    state["retired_submissions"] = sorted(retired, key=str)
    return state


def load_student_names(metadata_path=None, state=None):
    """Load student names, usernames, and profile names from metadata."""
    try:
        import submission_loader
        import os

        config = load_config()
        if metadata_path is None:
            metadata_path = config.METADATA_FILE
        metadata = submission_loader.load_metadata(metadata_path)
        result = {}
        for sid, data in metadata.items():
            if not isinstance(data, dict):
                continue
            submitters = data.get(":submitters", [{}])
            name = submitters[0].get(":name", "Unknown") if submitters else "Unknown"
            email = submitters[0].get(":email", "") if submitters else ""
            username = email.split("@")[0] if email else ""
            sub_dir = os.path.join(config.SUBMISSIONS_DIR, sid)
            profile = submission_loader.load_profile_name(sub_dir)
            result[sid] = {
                "name": name,
                "username": username,
                "profile": profile or "",
                "student_id": data.get(":sid", ""),
            }
        
        # Trace retired submissions AND missing submissions to their latest versions
        if state:
            history_trace = submission_loader.build_history_trace_map(metadata)
            
            # Collect all submissions that need tracing:
            # 1. Explicitly retired submissions
            # 2. Submissions in state ratings but missing from current metadata
            submissions_to_trace = set(state.get("retired_submissions", []))
            
            # Add submissions from ratings that are missing from metadata
            for sid in state.get("ratings", {}).keys():
                if sid not in result:  # If not found in current metadata
                    submissions_to_trace.add(sid)
            
            # Now trace all collected submissions
            for sid_to_trace in submissions_to_trace:
                if sid_to_trace not in result:
                    # Extract numeric ID from submission ID
                    numeric_id = sid_to_trace.replace("submission_", "")
                    latest_sid = history_trace.get(numeric_id)
                    # If we found a traced submission and it has data, fill in the entry
                    if latest_sid and latest_sid in result:
                        try:
                            latest_profile = submission_loader.load_profile_name(
                                os.path.join(config.SUBMISSIONS_DIR, latest_sid)
                            )
                            result[sid_to_trace] = {
                                "name": result[latest_sid]["name"],
                                "username": result[latest_sid]["username"],
                                "profile": latest_profile or result[latest_sid]["name"],
                                "student_id": result[latest_sid]["student_id"],
                            }
                        except Exception:
                            # Fall back to "Unknown" if tracing fails
                            pass
        
        return result
    except:
        return {}


def compute_conservative_rating(mu, sigma):
    return mu - 3 * sigma


def generate_leaderboard(state, state_file="tournament_state.json"):
    """
    Generate leaderboard with student-level deduplication.

    For students with multiple submissions, keeps only the submission with
    highest (frozen_cons, cons) score. Retired submissions are excluded.
    """
    # Load submission-to-student mapping for deduplication
    try:
        from submission_loader import load_metadata, build_submission_to_student_map

        config = load_config()
        metadata = load_metadata(config.METADATA_FILE)
        sub_to_student = build_submission_to_student_map(metadata)
    except Exception as e:
        logger.warning(f"Failed to load student mapping for deduplication: {e}")
        sub_to_student = {}

    # Get retired submissions to exclude from leaderboard
    retired = set(state.get("retired_submissions", []))

    config = load_config()
    names = load_student_names(state=state)
    frozen_scores = state.get("frozen_conservative", {})
    data = []
    for sid, ratings in state.get("ratings", {}).items():
        mu, sigma = (
            ratings.get("mu", config.TS_MU),
            ratings.get("sigma", config.TS_SIGMA),
        )
        current_cons = compute_conservative_rating(mu, sigma)
        frozen_cons = frozen_scores.get(sid, current_cons)
        rec = state.get("records", {}).get(sid, {"wins": 0, "losses": 0, "draws": 0})
        info = names.get(sid, {"name": "Unknown", "username": "", "profile": ""})
        data.append(
            {
                "sid": sid,
                "name": info["name"],
                "username": info["username"],
                "profile": info["profile"].strip() or info["name"],
                "mu": mu,
                "sigma": sigma,
                "frozen_cons": frozen_cons,
                "cons": current_cons,
                "w": rec.get("wins", 0),
                "l": rec.get("losses", 0),
                "d": rec.get("draws", 0),
            }
        )

    # Filter out retired submissions
    data = [entry for entry in data if entry["sid"] not in retired]

    # Deduplicate by student: keep submission with highest (frozen_cons, cons)
    if sub_to_student:
        student_best = {}  # student_id -> best submission entry
        for entry in data:
            sid = entry["sid"]
            student_id = sub_to_student.get(sid)
            if student_id is None:
                # No student mapping, keep as-is
                student_best[sid] = entry
                continue

            if student_id not in student_best:
                student_best[student_id] = entry
            else:
                # Compare: prefer higher frozen_cons, then higher cons
                current_best = student_best[student_id]
                if (entry["frozen_cons"], entry["cons"]) > (
                    current_best["frozen_cons"],
                    current_best["cons"],
                ):
                    student_best[student_id] = entry

        # Rebuild data with only best submissions per student
        data = list(student_best.values())
    data.sort(key=lambda x: (-x["frozen_cons"], -x["cons"]))

    header = (
        f"{'Rank':>3} | {'Name':20} | {'Username':15} | {'Profile':30} | "
        f"{'Submission ID':20} | {'Rating (mu+/-sigma)':16} | {'Frozen':6} | {'Current':7} | {'Record'}"
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
    for rank, e in enumerate(data, 1):
        lines.append(
            f"{rank:4} | {e['name']:20} | {e['username']:15} | {e['profile']:30} | {e['sid']:18} | {e['mu']:9.1f}+/-{e['sigma']:7.1f} | {e['frozen_cons']:6.1f} | {e['cons']:7.1f} | {e['w']}-{e['l']}-{e['d']}"
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
    with open(args.leaderboard, "w") as f:
        f.write(generate_leaderboard(state, args.state))


if __name__ == "__main__":
    main()
