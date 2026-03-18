"""
Tournament Orchestrator - Main script for running Breakthrough tournaments.

Coordinates matchmaking, parallel match execution, and result collection.
Uses ProcessPoolExecutor for cross-platform parallel match execution.

Usage:
    # Run 8 rounds with 4 workers
    python run_tournament.py --rounds 8 --workers 4

    # Add new submission and run 3 rounds
    python run_tournament.py --rounds 3 --add-submission submission_NEW

    # Use custom state file
    python run_tournament.py --rounds 4 --state custom_state.json
"""

import argparse
import concurrent.futures
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tournament_config import (
    SUBMISSIONS_DIR,
    METADATA_FILE,
    RESULTS_DIR,
    STATE_FILE,
    LEADERBOARD_FILE,
    MIN_SCORE,
    MAX_PARALLEL_WORKERS,
    GAMES_PER_PAIRING,
    trueskill_env,
    TS_MU,
    TS_SIGMA,
)
from submission_loader import (
    load_all_eligible,
    load_metadata,
    build_submission_to_student_map,
    get_eligible_submissions,
)
from matchmaker import generate_matchups, load_tournament_state
from result_collector import (
    collect_results,
    check_and_retire_lower_ranked,
    save_state,
    generate_leaderboard,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_match(match_dict: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    """
    Execute a single match via match_executor.py.

    Args:
        match_dict: Dictionary with keys:
            - 'white': white player submission ID
            - 'black': black player submission ID (or None for bye)
            - 'round': round number
            - 'match_id': unique match identifier

    Returns:
        Tuple of (match_id, error_message or None)
    """
    white = match_dict["white"]
    black = match_dict["black"]
    round_num = match_dict["round"]
    match_id = match_dict["match_id"]

    # Handle bye round (player has no opponent)
    if black is None:
        logger.info(f"Bye: {white} (round {round_num})")
        return match_id, None

    try:
        # Call match_executor.py with subprocess
        # Call match_executor.py with subprocess using sys.executable to ensure correct Python env
        result = subprocess.run(
            [
                sys.executable,  # Use current Python interpreter (respects venv)
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
            timeout=60000,
        )

        if result.returncode == 0:
            logger.info(f"Match {match_id}: {white} vs {black} completed")
            return match_id, None
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            logger.error(f"Match {match_id} failed: {error_msg}")
            return match_id, error_msg

    except subprocess.TimeoutExpired:
        error_msg = "Match timeout (>10 minutes)"
        logger.error(f"Match {match_id}: {error_msg}")
        return match_id, error_msg
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Match {match_id} execution error: {error_msg}")
        return match_id, error_msg


def execute_round_parallel(
    matches: List[Dict[str, Any]], workers: int
) -> Dict[str, Optional[str]]:
    """
    Execute all matches in a round using parallel workers.

    Args:
        matches: List of match dictionaries
        workers: Number of parallel workers

    Returns:
        Dictionary mapping match_id to error message (None if successful)
    """
    results = {}
    # Use ProcessPoolExecutor (cross-platform)
    logger.info(
        f"Executing {len(matches)} matches with {workers} parallel workers (ProcessPool)"
    )

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        # Submit all matches
        futures = {executor.submit(run_match, m): m for m in matches}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            match = futures[future]
            try:
                match_id, error = future.result()
                results[match_id] = error
                if error:
                    logger.warning(f"Match {match_id} had error: {error}")
            except Exception as e:
                logger.error(f"Future result error: {e}")
                results[match.get("match_id", "unknown")] = str(e)
    return results


def add_new_submission(submission_id: str, state_file: str) -> bool:
    """
    Add a new submission to the tournament state with default rating.

    Args:
        submission_id: New submission ID to add
        state_file: Path to tournament state file

    Returns:
        True if successful, False otherwise
    """
    try:
        state = load_tournament_state(state_file)

        # Check if already exists
        if submission_id in state.get("ratings", {}):
            logger.warning(f"Submission {submission_id} already in state")
            return True

        # Initialize with default TrueSkill rating
        state["ratings"][submission_id] = {
            "mu": TS_MU,
            "sigma": TS_SIGMA,
        }

        # Initialize record
        if "records" not in state:
            state["records"] = {}
        state["records"][submission_id] = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
        }

        # Save state
        if not save_state(state, state_file):
            logger.error(f"Failed to save state after adding {submission_id}")
            return False

        logger.info(
            f"Added submission {submission_id} with default rating (μ={TS_MU}, σ={TS_SIGMA})"
        )
        return True

    except Exception as e:
        logger.error(f"Failed to add submission {submission_id}: {e}")
        return False


def get_top_players(state: Dict[str, Any], n: int = 5) -> List[Tuple[str, float]]:
    """
    Get top N players by conservative rating (μ - 3σ).

    Args:
        state: Tournament state dictionary
        n: Number of top players to return

    Returns:
        List of (submission_id, conservative_rating) tuples, sorted highest first
    """
    ratings = state.get("ratings", {})
    players = []

    for sid, rating_dict in ratings.items():
        mu = rating_dict.get("mu", TS_MU)
        sigma = rating_dict.get("sigma", TS_SIGMA)
        cons_rating = mu - 3 * sigma
        players.append((sid, cons_rating))

    players.sort(key=lambda x: x[1], reverse=True)
    return players[:n]


def get_biggest_upset(
    state: Dict[str, Any], round_num: int
) -> Optional[Tuple[str, float]]:
    """
    Find biggest rating change in the round (biggest upset).

    Args:
        state: Tournament state dictionary
        round_num: Round number to analyze

    Returns:
        Tuple of (submission_id, rating_change) or None
    """
    # This would require tracking before/after ratings per round
    # For simplicity, return None (would require enhanced state tracking)
    return None


def print_round_summary(state: Dict[str, Any], round_num: int):
    """
    Print summary stats for a completed round.

    Args:
        state: Tournament state dictionary
        round_num: Round number
    """
    top_5 = get_top_players(state, 5)

    print(f"\n{'=' * 80}")
    print(f"ROUND {round_num} COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nTop 5 Players (Conservative Rating):")
    for i, (sid, cons_rating) in enumerate(top_5, 1):
        rating = state["ratings"].get(sid, {})
        mu = rating.get("mu", 0)
        sigma = rating.get("sigma", 0)
        rec = state.get("records", {}).get(sid, {"wins": 0, "losses": 0, "draws": 0})
        print(
            f"  {i}. {sid:20} | mu={mu:6.1f}+-{sigma:4.1f} | cons={cons_rating:6.1f} | "
            f"W-L-D: {rec['wins']}-{rec['losses']}-{rec['draws']}"
        )
    print()


def print_final_leaderboard(state: Dict[str, Any]):
    """
    Print final tournament leaderboard.

    Args:
        state: Tournament state dictionary
    """
    leaderboard = generate_leaderboard(state)
    print("\n" + leaderboard)


def validate_args(args) -> bool:
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments

    Returns:
        True if valid, False otherwise
    """
    # Allow rounds >= 0 when --break-ties is set (supports tiebreaker-only runs)
    if args.rounds < 0:
        logger.error(
            "--rounds must be >= 0 (use --rounds 0 --break-ties to run only tiebreakers)"
        )
        return False
    if args.rounds == 0 and not getattr(args, "break_ties", False):
        logger.error("--rounds 0 requires --break-ties flag")
        return False

    if args.workers < 1:
        logger.error("--workers must be >= 1")
        return False

    if not os.path.exists(args.state):
        logger.warning(
            f"State file {args.state} does not exist. Will create new state."
        )

    return True


def main():
    """Main tournament orchestrator."""
    parser = argparse.ArgumentParser(
        description="Run Breakthrough tournament with parallel match execution"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        required=True,
        help="Number of rounds to run",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_PARALLEL_WORKERS,
        help=f"Number of parallel workers (default: {MAX_PARALLEL_WORKERS})",
    )
    parser.add_argument(
        "--add-submission",
        type=str,
        default=None,
        help="Add new submission with submission ID before running",
    )
    parser.add_argument(
        "--state",
        type=str,
        default=STATE_FILE,
        help=f"Path to tournament state file (default: {STATE_FILE})",
    )
    parser.add_argument(
        "--break-ties",
        action="store_true",
        help="Run tiebreaker rounds to resolve rating ties after main tournament",
    )
    parser.add_argument(
        "--max-tb-iterations",
        type=int,
        default=5,
        help="Maximum tiebreaker iterations (default: 5)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not validate_args(args):
        sys.exit(1)

    logger.info(f"Tournament Configuration:")
    logger.info(f"  Rounds: {args.rounds}")
    logger.info(f"  Workers: {args.workers}")
    logger.info(f"  State file: {args.state}")

    # Load or create tournament state
    state = load_tournament_state(args.state)
    current_round = state.get("round_number", 1)

    # Perform roster sync with current Gradescope export
    logger.info("Performing roster sync with current Gradescope export...")
    metadata = load_metadata(METADATA_FILE)
    sub_to_student = build_submission_to_student_map(metadata)
    state.setdefault("submission_ownership", {})
    ownership = state.get("submission_ownership", {})
    if not isinstance(ownership, dict):
        ownership = {}
    ownership_updated = False
    for sub_id, student_id in sub_to_student.items():
        if student_id and ownership.get(sub_id) != student_id:
            ownership[sub_id] = student_id
            ownership_updated = True
    for sub_id in state.get("ratings", {}):
        unknown_owner = f"unknown:{sub_id}"
        if sub_id not in ownership:
            ownership[sub_id] = unknown_owner
            ownership_updated = True
    state["submission_ownership"] = ownership

    eligible = set(get_eligible_submissions(metadata, MIN_SCORE))
    pending = set(state.get("pending_retirement", []))
    retired_all = set(state.get("retired_submissions", []))
    reactivated = retired_all & pending
    retired = retired_all - pending
    retired_updated = retired != retired_all
    state["retired_submissions"] = sorted(retired)

    logger.info(f"Eligible submissions in current export: {len(eligible)}")
    logger.info(f"Retired submissions (permanent dropouts): {len(retired)}")
    logger.info(f"Pending retirement submissions: {len(pending)}")
    if reactivated:
        logger.info(
            f"Reactivated {len(reactivated)} pending submission(s) previously marked retired"
        )

    # Add new submissions not yet in state
    new_added = 0
    for sub_id in eligible:
        if sub_id not in state.get("ratings", {}) and sub_id not in retired:
            state["ratings"][sub_id] = {"mu": TS_MU, "sigma": TS_SIGMA}
            state.setdefault("records", {})[sub_id] = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
            }
            logger.info(f"Added new submission: {sub_id}")
            new_added += 1

    if new_added > 0 or retired_updated or ownership_updated:
        # Save updated state after roster sync mutations
        if not save_state(state, args.state):
            logger.error("Failed to save state after roster sync")
            sys.exit(1)

    logger.info(f"Added {new_added} new submissions to tournament")
    total_ratings = len(state.get("ratings", {}))
    active_players = len([s for s in state["ratings"] if s not in retired])
    logger.info(f"Total rated submissions: {total_ratings}")
    logger.info(f"Active roster size (including pending): {active_players}")

    # Add new submission if requested
    if args.add_submission:
        logger.info(f"Adding new submission: {args.add_submission}")
        if not add_new_submission(args.add_submission, args.state):
            logger.error(f"Failed to add submission {args.add_submission}")
            sys.exit(1)
        state = load_tournament_state(args.state)

    # Initialize state with all eligible submissions if state is empty
    if not state.get("ratings", {}):
        logger.info("Initializing tournament state with eligible submissions...")
        eligible = load_all_eligible(SUBMISSIONS_DIR, METADATA_FILE)
        logger.info(f"Found {len(eligible)} eligible submissions")

        for sub_id in eligible:
            state["ratings"][sub_id] = {"mu": TS_MU, "sigma": TS_SIGMA}
            if "records" not in state:
                state["records"] = {}
            state["records"][sub_id] = {"wins": 0, "losses": 0, "draws": 0}

        if not save_state(state, args.state):
            logger.error("Failed to save initial state")
            sys.exit(1)
        logger.info(
            f"Initialized {len(eligible)} submissions with default TrueSkill ratings"
        )
    # Ensure results directory exists
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Run tournament rounds
    for round_num in range(current_round, current_round + args.rounds):
        logger.info(f"\n{'=' * 80}")
        logger.info(f"ROUND {round_num} START")
        logger.info(f"{'=' * 80}")

        # Step 1: Generate matchups
        logger.info(f"Generating matchups for round {round_num}...")
        matches = generate_matchups(
            round_num, args.state, student_map=sub_to_student, retired=retired
        )
        logger.info(f"Generated {len(matches)} matches")

        if not matches:
            logger.warning(f"No matches generated for round {round_num}. Skipping.")
            continue

        # Step 2: Execute matches in parallel
        logger.info(f"Executing {len(matches)} matches in parallel...")
        match_results = execute_round_parallel(matches, args.workers)

        # Log any failures
        failures = {mid: err for mid, err in match_results.items() if err}
        if failures:
            logger.warning(f"{len(failures)} matches had errors:")
            for mid, err in list(failures.items())[:5]:
                logger.warning(f"  {mid}: {err}")

        # Step 3: Collect results and update ratings
        logger.info(f"Collecting results for round {round_num}...")
        state = collect_results(round_num, args.state)
        state = check_and_retire_lower_ranked(state)

        if not save_state(state, args.state):
            logger.error(f"Failed to save state after round {round_num}")
            sys.exit(1)

        # Step 4: Print round summary
        print_round_summary(state, round_num)

    # Generate final leaderboard after all rounds
    logger.info("Generating final leaderboard...")
    leaderboard = generate_leaderboard(state, args.state)
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            f.write(leaderboard)
        logger.info(f"Final leaderboard saved: {LEADERBOARD_FILE}")
    except Exception as e:
        logger.error(f"Failed to write leaderboard: {e}")

    # Run tiebreakers if requested
    if args.break_ties:
        logger.info("\n" + "=" * 80)
        logger.info("STARTING TIEBREAKER SYSTEM")
        logger.info("=" * 80)

        from tiebreaker import run_tiebreakers

        result = run_tiebreakers(
            state_file=args.state,
            workers=args.workers,
            max_iterations=args.max_tb_iterations,
            precision=2,
            dry_run=False,
        )

        if result["success"]:
            logger.info(
                f"✓ All ties resolved after {result['iterations']} iteration(s)!"
            )
        else:
            logger.warning(
                f"⚠ {result['final_ties']} tied groups remaining after "
                f"{result['iterations']} iteration(s). Consider increasing --max-tb-iterations."
            )

        # Reload state and regenerate leaderboard
        state = load_tournament_state(args.state)
        leaderboard = generate_leaderboard(state, args.state)
        try:
            with open(LEADERBOARD_FILE, "w") as f:
                f.write(leaderboard)
            logger.info(f"Updated leaderboard after tiebreakers: {LEADERBOARD_FILE}")
        except Exception as e:
            logger.error(f"Failed to write leaderboard: {e}")
    # Print final leaderboard
    logger.info(f"\nTournament complete! Final standings:")
    print_final_leaderboard(state)

    logger.info(f"\nResults saved to: {RESULTS_DIR}")
    logger.info(f"Leaderboard saved to: {LEADERBOARD_FILE}")
    logger.info(f"State saved to: {args.state}")


if __name__ == "__main__":
    main()
