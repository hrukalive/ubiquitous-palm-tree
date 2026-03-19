"""
Main tournament orchestrator for Breakthrough submissions.
"""

import argparse
import concurrent.futures
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

from matchmaker import generate_matchups, load_tournament_state
from result_collector import collect_results, generate_leaderboard, save_state
from submission_loader import get_eligible_submissions, load_all_metadata
from tiebreaker import run_tiebreakers
from tournament_config import (
    GAME_TIMEOUT,
    LEADERBOARD_FILE,
    MAX_PARALLEL_WORKERS,
    MIN_SCORE,
    RESULTS_DIR,
    STATE_FILE,
    SUBMISSIONS_DIR,
    TIEBREAK_FILE,
    TS_MU,
    TS_SIGMA,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_match(match_dict: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    white = match_dict["white"]
    black = match_dict["black"]
    round_num = match_dict["round"]
    match_id = match_dict["match_id"]

    if black is None:
        logger.info("Bye: %s (round %s)", white, round_num)
        return match_id, None

    try:
        result = subprocess.run(
            [
                sys.executable,
                "match_executor.py",
                "--white",
                white,
                "--black",
                black,
                "--round",
                str(round_num),
                "--match-id",
                match_id,
            ],
            capture_output=True,
            text=True,
            timeout=GAME_TIMEOUT + 60,
        )

        if result.returncode == 0:
            logger.info("Match %s: %s vs %s completed", match_id, white, black)
            return match_id, None

        error_msg = result.stderr or result.stdout or "Unknown error"
        logger.error("Match %s failed: %s", match_id, error_msg)
        return match_id, error_msg

    except subprocess.TimeoutExpired:
        error_msg = f"Match timeout (>{GAME_TIMEOUT}s)"
        logger.error("Match %s: %s", match_id, error_msg)
        return match_id, error_msg
    except Exception as exc:
        error_msg = str(exc)
        logger.error("Match %s execution error: %s", match_id, error_msg)
        return match_id, error_msg


def execute_round_parallel(
    matches: List[Dict[str, Any]], workers: int
) -> Dict[str, Optional[str]]:
    results = {}
    logger.info(
        "Executing %s matches with %s parallel workers", len(matches), workers
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_match, match): match for match in matches}
        for future in concurrent.futures.as_completed(futures):
            match = futures[future]
            try:
                match_id, error = future.result()
                results[match_id] = error
                if error:
                    logger.warning("Match %s had error: %s", match_id, error)
            except Exception as exc:
                logger.error("Future result error: %s", exc)
                results[match.get("match_id", "unknown")] = str(exc)
    return results


def add_new_submission(submission_id: str, state_file: str) -> bool:
    state = load_tournament_state(state_file)
    if submission_id in state.get("ratings", {}):
        logger.warning("Submission %s already in state", submission_id)
        return True

    state.setdefault("ratings", {})[submission_id] = {"mu": TS_MU, "sigma": TS_SIGMA}
    state.setdefault("records", {})[submission_id] = {
        "wins": 0,
        "losses": 0,
        "draws": 0,
    }
    if not save_state(state, state_file):
        logger.error("Failed to save state after adding %s", submission_id)
        return False
    logger.info("Added submission %s with default rating", submission_id)
    return True


def sync_state_with_exports(state: Dict[str, Any]) -> Tuple[Dict[str, Any], int, int]:
    metadata = load_all_metadata(SUBMISSIONS_DIR)
    eligible = get_eligible_submissions(metadata, MIN_SCORE)
    new_added = 0

    state.setdefault("ratings", {})
    state.setdefault("records", {})

    for submission_id in eligible:
        if submission_id in state["ratings"]:
            continue
        state["ratings"][submission_id] = {"mu": TS_MU, "sigma": TS_SIGMA}
        state["records"][submission_id] = {"wins": 0, "losses": 0, "draws": 0}
        new_added += 1

    return state, len(eligible), new_added


def print_round_summary(state: Dict[str, Any], round_num: int):
    top_players = []
    for submission_id, rating in state.get("ratings", {}).items():
        mu = rating.get("mu", TS_MU)
        sigma = rating.get("sigma", TS_SIGMA)
        top_players.append((submission_id, mu - 3 * sigma, mu, sigma))
    top_players.sort(key=lambda item: item[1], reverse=True)

    print(f"\n{'=' * 80}")
    print(f"ROUND {round_num} COMPLETE")
    print(f"{'=' * 80}")
    for idx, (submission_id, score, mu, sigma) in enumerate(top_players[:5], start=1):
        record = state.get("records", {}).get(
            submission_id, {"wins": 0, "losses": 0, "draws": 0}
        )
        print(
            f"  {idx}. {submission_id:20} | score={score:7.2f} | "
            f"mu={mu:7.2f} sigma={sigma:6.2f} | "
            f"{record['wins']}-{record['losses']}-{record['draws']}"
        )


def print_final_leaderboard(
    state: Dict[str, Any], tiebreak_results: Optional[Dict[str, Any]]
):
    print("\n" + generate_leaderboard(state, tiebreak_results))


def validate_args(args) -> bool:
    if args.rounds < 0:
        logger.error("--rounds must be >= 0")
        return False
    if args.rounds == 0 and not args.break_ties:
        logger.error("--rounds 0 requires --break-ties")
        return False
    if args.workers < 1:
        logger.error("--workers must be >= 1")
        return False
    if not os.path.exists(args.state):
        logger.warning("State file %s does not exist. Will create new state.", args.state)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run Breakthrough tournaments across all discovered exports"
    )
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--workers", type=int, default=MAX_PARALLEL_WORKERS)
    parser.add_argument("--add-submission", type=str, default=None)
    parser.add_argument("--state", type=str, default=STATE_FILE)
    parser.add_argument(
        "--break-ties",
        action="store_true",
        help="Run a fresh temporary tiebreak ladder for equal-score groups",
    )
    args = parser.parse_args()

    if not validate_args(args):
        sys.exit(1)

    logger.info("Submissions root: %s", SUBMISSIONS_DIR)
    logger.info("State file: %s", args.state)
    logger.info("Rounds: %s", args.rounds)
    logger.info("Workers: %s", args.workers)

    state = load_tournament_state(args.state)
    state, eligible_count, new_added = sync_state_with_exports(state)
    logger.info("Discovered %s eligible submissions across all exports", eligible_count)
    logger.info("Added %s new submissions to the state", new_added)

    if args.add_submission:
        if not add_new_submission(args.add_submission, args.state):
            sys.exit(1)
        state = load_tournament_state(args.state)

    if not save_state(state, args.state):
        logger.error("Failed to save state after export sync")
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    current_round = state.get("round_number", 1)

    for round_num in range(current_round, current_round + args.rounds):
        logger.info("\n%s", "=" * 80)
        logger.info("ROUND %s START", round_num)
        logger.info("%s", "=" * 80)

        matches = generate_matchups(round_num, args.state)
        logger.info("Generated %s matches", len(matches))
        if not matches:
            logger.warning("No matches generated for round %s", round_num)
            continue

        match_results = execute_round_parallel(matches, args.workers)
        failures = {match_id: error for match_id, error in match_results.items() if error}
        if failures:
            logger.warning("%s matches had errors", len(failures))

        state = collect_results(round_num, args.state)
        if not save_state(state, args.state):
            logger.error("Failed to save state after round %s", round_num)
            sys.exit(1)

        print_round_summary(state, round_num)

    state = load_tournament_state(args.state)
    tiebreak_results = None
    if args.break_ties:
        tiebreak_results = run_tiebreakers(
            state_file=args.state,
            output_file=TIEBREAK_FILE,
        )
        logger.info("Saved temporary tiebreak results to %s", TIEBREAK_FILE)

    leaderboard = generate_leaderboard(state, tiebreak_results)
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            f.write(leaderboard)
        logger.info("Final leaderboard saved to %s", LEADERBOARD_FILE)
    except Exception as exc:
        logger.error("Failed to write leaderboard: %s", exc)

    print_final_leaderboard(state, tiebreak_results)
    logger.info("Results saved to: %s", RESULTS_DIR)
    logger.info("State saved to: %s", args.state)


if __name__ == "__main__":
    main()
