"""
Tiebreaker Orchestrator - Run additional rounds to resolve rating ties.

This module coordinates tiebreaker mini-tournaments for groups of players with
identical TrueSkill ratings. Runs Swiss-style matchups within each tied group
until all ratings are unique or max iterations reached.

Usage:
    From run_tournament.py:
        from tiebreaker import run_tiebreakers
        result = run_tiebreakers(state_file="tournament_state.json", workers=4)

    Standalone:
        python tiebreaker.py --state tournament_state.json --workers 4
"""

import json
import os
import sys
import shutil
import logging
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed

from tie_detector import detect_ties, summarize_ties
from matchmaker import generate_tiebreaker_matchups
from result_collector import collect_tiebreaker_results, load_state, save_state
from tournament_config import RESULTS_DIR, MAX_PARALLEL_WORKERS, GAME_TIMEOUT, METADATA_FILE, MIN_SCORE
from submission_loader import load_metadata, build_submission_to_student_map

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tiebreaker configuration
TIEBREAKER_ROUND_BASE = 100  # Start tiebreaker rounds at 100
DEFAULT_MAX_ITERATIONS = 5  # Max tiebreaker iterations before giving up
DEFAULT_PRECISION = 2  # Decimal places for tie detection


def _backup_state(state_file: str) -> str:
    """
    Create backup of tournament state before running tiebreakers.

    Args:
        state_file: Path to tournament state JSON

    Returns:
        Path to backup file

    Example:
        >>> backup_path = _backup_state("tournament_state.json")
        >>> print(backup_path)
        tournament_state_pre_tiebreak.json
    """
    backup_file = state_file.replace(".json", "_pre_tiebreak.json")
    shutil.copy2(state_file, backup_file)
    logger.info(f"Created state backup: {backup_file}")
    return backup_file


def _generate_all_group_matchups(
    tied_groups: List[List[str]],
    state: Dict[str, Any],
    round_num: int,
    seed: int = 42,
    student_map: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate matchups for all tied groups in a single round.

    Args:
        tied_groups: List of tied player groups from detect_ties()
        state: Tournament state dict
        round_num: Tiebreaker round number (100+)
        seed: Random seed for reproducibility
        student_map: Optional dict mapping submission_id → student_id for anti-matching

    Returns:
        Combined list of all matches across all groups with unique match IDs

    Example:
        >>> tied_groups = [["p1", "p2"], ["p3", "p4", "p5"]]
        >>> matches = _generate_all_group_matchups(tied_groups, state, 100)
        >>> len(matches)  # 2*2 (group 1) + 2*2 + 1 bye (group 2)
        7
    """
    all_matches = []
    match_id_offset = 0

    for group_idx, group_players in enumerate(tied_groups):
        logger.info(
            f"  Group {group_idx + 1}: Generating matchups for {len(group_players)} players"
        )

        # Generate matchups for this group
        group_matches = generate_tiebreaker_matchups(
            players=group_players,
            state=state,
            round_num=round_num,
            match_id_offset=match_id_offset,
            seed=seed + group_idx,  # Unique seed per group
            student_map=student_map,
        )

        all_matches.extend(group_matches)
        match_id_offset += len(group_matches)

    return all_matches


def _execute_matches_parallel(
    matches: List[Dict[str, Any]],
    round_num: int,
    workers: int,
) -> Tuple[int, int]:
    """
    Execute tiebreaker matches in parallel using ProcessPoolExecutor.

    Args:
        matches: List of match dicts from generate_tiebreaker_matchups()
        round_num: Tiebreaker round number (100+)
        workers: Number of parallel workers

    Returns:
        Tuple of (successes, failures) counts

    Note:
        This function shells out to match_executor.py for each match.
        Results are written to results/round_XXX/ directory.
    """
    import subprocess

    # Create round directory
    round_dir = Path(RESULTS_DIR) / f"round_{round_num:02d}"
    round_dir.mkdir(parents=True, exist_ok=True)

    # Write matches.json for reference
    matches_file = round_dir / "matches.json"
    with open(matches_file, "w") as f:
        json.dump(matches, f, indent=2)

    logger.info(
        f"Executing {len(matches)} tiebreaker matches with {workers} workers..."
    )

    successes = 0
    failures = 0

    # Filter out bye matches (black=None)
    real_matches = [m for m in matches if m.get("black") is not None]

    if not real_matches:
        logger.info("No real matches to execute (all byes)")
        return 0, 0

    # Execute matches in parallel
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []

        for match in real_matches:
            # Call match_executor.py as subprocess
            cmd = [
                sys.executable,  # Use current Python interpreter (respects venv)
                "match_executor.py",
                "--white",
                match["white"],
                "--black",
                match["black"],
                "--round",
                str(round_num),
                "--match-id",
                match["match_id"],
            ]

            future = executor.submit(
                subprocess.run, cmd, capture_output=True, text=True
            )
            futures.append((future, match["match_id"]))

        # Collect results
        for future, match_id in futures:
            try:
                result = future.result(timeout=GAME_TIMEOUT + 60)  # +60s overhead
                if result.returncode == 0:
                    # Extract white and black from match
                    match = next(m for m in real_matches if m["match_id"] == match_id)
                    logger.info(
                        f"Match {match_id}: {match['white']} vs {match['black']} completed"
                    )
                    successes += 1
                else:
                    logger.error(f"Match {match_id} failed: {result.stderr}")
                    failures += 1
            except Exception as e:
                logger.error(f"Match {match_id} exception: {e}")
                failures += 1

    return successes, failures


def _print_iteration_summary(
    iteration: int,
    round_num: int,
    tied_groups: List[List[str]],
    state: Dict[str, Any],
    successes: int,
    failures: int,
):
    """
    Print human-readable summary of a tiebreaker iteration.

    Args:
        iteration: Iteration number (1-indexed)
        round_num: Tiebreaker round number (100+)
        tied_groups: List of tied groups before this iteration
        state: Tournament state after processing results
        successes: Number of successful matches
        failures: Number of failed matches
    """
    print("\n" + "=" * 80)
    print(f"TIEBREAKER ITERATION {iteration} (Round {round_num}) - SUMMARY")
    print("=" * 80)
    print(f"Tied groups at start: {len(tied_groups)}")
    print(f"Players involved: {sum(len(g) for g in tied_groups)}")
    print(f"Matches executed: {successes} successful, {failures} failed")

    # Check remaining ties
    new_tied_groups = detect_ties(state, precision=DEFAULT_PRECISION)
    print(f"\nTied groups remaining: {len(new_tied_groups)}")
    print(f"Players still tied: {sum(len(g) for g in new_tied_groups)}")

    if new_tied_groups:
        print("\nRemaining ties:")
        print(summarize_ties(state, new_tied_groups))
    else:
        print("\nAll ties resolved!")

    print("=" * 80 + "\n")


def run_tiebreakers(
    state_file: str = "tournament_state.json",
    workers: int = MAX_PARALLEL_WORKERS,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    precision: int = DEFAULT_PRECISION,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Run tiebreaker rounds to resolve all rating ties.

    This is the main entry point for the tiebreaker system. Iteratively runs
    Swiss-style mini-tournaments within tied groups until all ratings are unique
    or max iterations reached.

    Args:
        state_file: Path to tournament state JSON (default: tournament_state.json)
        workers: Number of parallel match workers (default: from config)
        max_iterations: Max tiebreaker iterations (default: 5)
        precision: Decimal places for tie detection (default: 2)
        dry_run: If True, only detect ties without running matches

    Returns:
        Dict with keys:
            - "success": bool (True if all ties resolved)
            - "iterations": int (number of iterations run)
            - "initial_ties": int (tied groups at start)
            - "final_ties": int (tied groups remaining)
            - "backup_file": str (path to pre-tiebreak backup)

    Example:
        >>> result = run_tiebreakers("tournament_state.json", workers=4, max_iterations=5)
        >>> if result["success"]:
        ...     print("All ties resolved!")
        >>> else:
        ...     print(f"{result['final_ties']} tied groups remaining after {result['iterations']} iterations")
    """
    logger.info("=" * 80)
    logger.info("TIEBREAKER SYSTEM - Starting")
    logger.info("=" * 80)

    # Load initial state
    state = load_state(state_file)
    initial_round_number = state.get("round_number", 1)

    # Load metadata and build student mapping for anti-matching
    try:
        metadata = load_metadata(METADATA_FILE)
        sub_to_student = build_submission_to_student_map(metadata)
        logger.info(f"Loaded student mapping for {len(sub_to_student)} submissions")
    except Exception as e:
        logger.warning(f"Failed to load student mapping: {e}. Same-student anti-matching disabled.")
        sub_to_student = None

    # Freeze pre-tiebreak conservative scores once for stable leaderboard ranking
    if "frozen_conservative" not in state:
        state["frozen_conservative"] = {}
        for player_id, rating in state.get("ratings", {}).items():
            mu = rating.get("mu", 25.0)
            sigma = rating.get("sigma", 8.333)
            state["frozen_conservative"][player_id] = mu - 3 * sigma

        if save_state(state, state_file):
            logger.info(
                f"Captured frozen conservative scores for {len(state['frozen_conservative'])} players"
            )
        else:
            logger.warning("Failed to persist frozen conservative scores")

    # Detect initial ties
    tied_groups = detect_ties(state, precision=precision)

    if not tied_groups:
        logger.info("No tied groups found. All ratings are already unique.")
        return {
            "success": True,
            "iterations": 0,
            "initial_ties": 0,
            "final_ties": 0,
            "backup_file": None,
        }

    logger.info(f"\nInitial tie analysis:")
    print(summarize_ties(state, tied_groups))

    if dry_run:
        logger.info("DRY RUN mode - Exiting without running matches")
        return {
            "success": False,
            "iterations": 0,
            "initial_ties": len(tied_groups),
            "final_ties": len(tied_groups),
            "backup_file": None,
        }

    # Create backup
    backup_file = _backup_state(state_file)

    # Run tiebreaker iterations
    iteration = 0
    previous_tie_count = len(tied_groups)

    while iteration < max_iterations and tied_groups:
        iteration += 1
        round_num = TIEBREAKER_ROUND_BASE + iteration - 1

        logger.info(f"\n{'=' * 80}")
        logger.info(f"TIEBREAKER ITERATION {iteration} (Round {round_num})")
        logger.info(f"{'=' * 80}")
        logger.info(
            f"Resolving {len(tied_groups)} tied groups involving {sum(len(g) for g in tied_groups)} players"
        )

        # Generate matchups for all groups
        all_matches = _generate_all_group_matchups(
            tied_groups=tied_groups,
            state=state,
            round_num=round_num,
            seed=42 + iteration,
            student_map=sub_to_student,
        )

        logger.info(f"Generated {len(all_matches)} total matches")

        # Execute matches in parallel
        successes, failures = _execute_matches_parallel(
            matches=all_matches,
            round_num=round_num,
            workers=workers,
        )

        # Collect results with tier isolation (updates state in-place, preserves round_number)
        state = collect_tiebreaker_results(
            round_num,
            state,
            RESULTS_DIR,
            tied_groups=tied_groups,
            precision=precision,
            enforce_tier_isolation=True,  # Enable tier-preserving mode
        )

        # Save updated state
        if not save_state(state, state_file):
            logger.error(f"Failed to save state after iteration {iteration}")
            break

        # Print summary
        _print_iteration_summary(
            iteration=iteration,
            round_num=round_num,
            tied_groups=tied_groups,
            state=state,
            successes=successes,
            failures=failures,
        )

        # Check for progress
        new_tied_groups = detect_ties(state, precision=precision)

        if not new_tied_groups:
            logger.info(f"Success! All ties resolved after {iteration} iteration(s)")
            break

        if len(new_tied_groups) == previous_tie_count:
            logger.warning(
                f"No progress made in iteration {iteration}. "
                f"Still {len(new_tied_groups)} tied groups. "
                f"This may indicate extremely similar skill levels."
            )
            # Continue anyway - sometimes ties persist but individual ratings shift

        previous_tie_count = len(new_tied_groups)
        tied_groups = new_tied_groups

    # Final summary
    final_tied_groups = detect_ties(state, precision=precision)

    logger.info("\n" + "=" * 80)
    logger.info("TIEBREAKER SYSTEM - Final Results")
    logger.info("=" * 80)
    logger.info(f"Iterations run: {iteration}")
    logger.info(
        f"Initial tied groups: {len(detect_ties(load_state(backup_file), precision))}"
    )
    logger.info(f"Final tied groups: {len(final_tied_groups)}")
    logger.info(
        f"Tournament round_number preserved: {state.get('round_number')} (initial: {initial_round_number})"
    )

    if final_tied_groups:
        logger.info("\nRemaining tied groups:")
        print(summarize_ties(state, final_tied_groups))

    success = len(final_tied_groups) == 0

    return {
        "success": success,
        "iterations": iteration,
        "initial_ties": len(detect_ties(load_state(backup_file), precision)),
        "final_ties": len(final_tied_groups),
        "backup_file": backup_file,
    }


def main():
    """CLI entry point for standalone tiebreaker execution."""
    parser = argparse.ArgumentParser(
        description="Run tiebreaker rounds to resolve rating ties"
    )
    parser.add_argument(
        "--state",
        type=str,
        default="tournament_state.json",
        help="Path to tournament state file (default: tournament_state.json)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_PARALLEL_WORKERS,
        help=f"Number of parallel workers (default: {MAX_PARALLEL_WORKERS})",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"Max tiebreaker iterations (default: {DEFAULT_MAX_ITERATIONS})",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=DEFAULT_PRECISION,
        help=f"Decimal places for tie detection (default: {DEFAULT_PRECISION})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only detect ties without running matches",
    )

    args = parser.parse_args()

    result = run_tiebreakers(
        state_file=args.state,
        workers=args.workers,
        max_iterations=args.max_iterations,
        precision=args.precision,
        dry_run=args.dry_run,
    )

    # Exit with appropriate code
    exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
