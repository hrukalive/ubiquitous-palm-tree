"""
Match Executor - CLI script to run a single Breakthrough match
between two student eval functions with timeout handling.

Usage:
    python match_executor.py --white SUBMISSION_ID --black SUBMISSION_ID --round N --match-id M

Example:
    python match_executor.py --white submission_391569593 --black submission_392481164 --round 3 --match-id 5
"""

import argparse
import json
import logging
import queue
import threading
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional, Tuple, Any, Callable

from tournament_config import (
    AGENT_DEPTH,
    MAX_MOVES,
    GAME_TIMEOUT,
    RESULTS_DIR,
    SUBMISSIONS_DIR,
)
from submission_loader import load_eval_fn
from breakthrough_internal import play_game, Breakthrough
from breakthrough_agent_internal import AlphaBetaAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_with_timeout(
    fn: Callable, args: Tuple, timeout_seconds: int
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Run a function with timeout using threading (Windows-compatible).

    Args:
        fn: Function to call
        args: Tuple of arguments to pass to fn
        timeout_seconds: Timeout in seconds

    Returns:
        Tuple of (result, error_message)
        - If successful: (result_value, None)
        - If timeout: (None, "Timeout after Xs")
        - If error: (None, error_message)
    """
    result_q = queue.Queue()

    def target():
        try:
            result = fn(*args)
            result_q.put(("ok", result))
        except Exception as e:
            result_q.put(("error", str(e)))

    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout=timeout_seconds)

    if t.is_alive():
        # Thread is still running after timeout
        return None, f"Timeout after {timeout_seconds}s"

    try:
        status, val = result_q.get_nowait()
        if status == "ok":
            return val, None
        else:
            return None, val
    except queue.Empty:
        return None, "Unknown error (queue empty)"


def load_eval_functions(
    white_id: str, black_id: str
) -> Tuple[Optional[Callable], Optional[Callable], Optional[str]]:
    """
    Load eval functions for both players.

    Args:
        white_id: White player submission ID
        black_id: Black player submission ID

    Returns:
        Tuple of (white_eval_fn, black_eval_fn, error_message)
        - If both load successfully: (white_fn, black_fn, None)
        - If either fails: (None, None, error_message)
    """
    logger.info(f"Loading eval functions for white={white_id}, black={black_id}")

    white_eval = load_eval_fn(white_id, SUBMISSIONS_DIR)
    if white_eval is None:
        return None, None, f"Failed to load white eval function from {white_id}"

    black_eval = load_eval_fn(black_id, SUBMISSIONS_DIR)
    if black_eval is None:
        return None, None, f"Failed to load black eval function from {black_id}"

    logger.info("Successfully loaded both eval functions")
    return white_eval, black_eval, None


def run_match(
    white_id: str, black_id: str, white_eval: Callable, black_eval: Callable
) -> Tuple[Optional[dict], Optional[str]]:
    """
    Run a single match between two agents.

    Args:
        white_id: White player submission ID
        black_id: Black player submission ID
        white_eval: White player eval function
        black_eval: Black player eval function

    Returns:
        Tuple of (result_dict, error_message)
        - If successful: (result_dict, None)
        - If timeout/error: (None, error_message)
    """
    logger.info(f"Creating agents for {white_id} vs {black_id}")

    try:
        # Create agents
        white_agent = AlphaBetaAgent(
            name=white_id, depth=AGENT_DEPTH, eval_fn=white_eval
        )
        black_agent = AlphaBetaAgent(
            name=black_id, depth=AGENT_DEPTH, eval_fn=black_eval
        )

        logger.info(
            f"Running match with timeout={GAME_TIMEOUT}s, max_moves={MAX_MOVES}"
        )

        # Run with timeout
        result, error = run_with_timeout(
            play_game,
            (white_agent, black_agent, MAX_MOVES),
            GAME_TIMEOUT,
        )

        if error:
            return None, error

        logger.info(
            f"Match completed: winner={result['winner']}, moves={result['total_moves']}"
        )
        return result, None

    except Exception as e:
        error_msg = f"Exception during match: {str(e)}"
        logger.error(error_msg)
        return None, error_msg


def clear_game_cache():
    """Clear LRU cache on Breakthrough.result for fresh match."""
    try:
        Breakthrough.result.cache_clear()
        logger.info("Cleared Breakthrough.result cache")
    except Exception as e:
        logger.warning(f"Could not clear cache: {e}")


def build_result_json(
    match_id: str,
    round_num: int,
    white_id: str,
    black_id: str,
    game_result: Optional[dict],
    error: Optional[str],
) -> dict:
    """
    Build the result JSON structure.

    Args:
        match_id: Match ID (e.g., "match_0003")
        round_num: Round number
        white_id: White submission ID
        black_id: Black submission ID
        game_result: Result dict from play_game, or None if error
        error: Error message, or None if successful

    Returns:
        Result dictionary
    """
    result = {
        "match_id": match_id,
        "round": round_num,
        "white_submission": white_id,
        "black_submission": black_id,
        "winner": None,
        "total_moves": None,
        "white_nodes": None,
        "black_nodes": None,
        "white_time_per_move": None,
        "black_time_per_move": None,
        "white_captures": None,
        "black_captures": None,
        "error": None,
        "timestamp": datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z"),
    }

    if game_result:
        result["winner"] = game_result["winner"]
        result["total_moves"] = game_result["total_moves"]
        result["white_nodes"] = game_result["white_nodes"]
        result["black_nodes"] = game_result["black_nodes"]
        result["white_time_per_move"] = game_result["white_time_per_move"]
        result["black_time_per_move"] = game_result["black_time_per_move"]
        result["white_captures"] = game_result["white_captures"]
        result["black_captures"] = game_result["black_captures"]
    elif error:
        result["error"] = error

    return result


def write_result(match_id: str, round_num: int, result: dict) -> str:
    """
    Write result JSON to file.

    Args:
        match_id: Match ID (e.g., "0003")
        round_num: Round number
        result: Result dictionary

    Returns:
        Path to written file

    Raises:
        OSError if write fails
    """
    round_dir = Path(RESULTS_DIR) / f"round_{round_num:02d}"
    round_dir.mkdir(parents=True, exist_ok=True)
    filepath = round_dir / f"{match_id}.json"

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    logger.info("Wrote result to %s", filepath)
    return str(filepath)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run a single Breakthrough match between two submissions"
    )
    parser.add_argument(
        "--white",
        required=True,
        help="White player submission ID (e.g., submission_391569593)",
    )
    parser.add_argument(
        "--black",
        required=True,
        help="Black player submission ID (e.g., submission_392481164)",
    )
    parser.add_argument(
        "--round", type=int, required=True, help="Round number (e.g., 3)"
    )
    parser.add_argument(
        "--match-id", type=str, required=True, help="Match ID string (e.g., match_0001)"
    )

    args = parser.parse_args()

    white_id = args.white
    black_id = args.black
    round_num = args.round
    match_id = args.match_id

    logger.info(
        f"Starting match: round={round_num}, match_id={match_id}, "
        f"white={white_id}, black={black_id}"
    )

    # Load eval functions
    white_eval, black_eval, load_error = load_eval_functions(white_id, black_id)

    if load_error:
        logger.error(f"Failed to load eval functions: {load_error}")
        result = build_result_json(
            match_id,
            round_num,
            white_id,
            black_id,
            None,
            load_error,
        )
        write_result(match_id, round_num, result)
        return 1

    # Clear cache before match
    clear_game_cache()

    # Run match
    game_result, match_error = run_match(white_id, black_id, white_eval, black_eval)

    # Build result
    result = build_result_json(
        match_id,
        round_num,
        white_id,
        black_id,
        game_result,
        match_error,
    )

    # Write result
    try:
        write_result(match_id, round_num, result)
    except OSError as e:
        logger.error(f"Failed to write result: {e}")
        return 1

    # Log summary
    if game_result:
        logger.info(f"Match completed successfully: {game_result['winner']} wins")
        return 0
    else:
        logger.error(f"Match failed: {match_error}")
        return 1


if __name__ == "__main__":
    exit(main())
