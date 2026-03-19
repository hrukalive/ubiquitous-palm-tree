"""
Temporary tiebreak tournament for submissions that share the same main score.

This module never mutates the main tournament ratings. It creates a separate
temporary TrueSkill ladder inside each tied group and uses that ladder only as
the second sort key for the final leaderboard.
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional

from match_executor import load_eval_functions, run_match
from matchmaker import generate_tiebreaker_matchups
from result_collector import (
    build_tiebreak_fingerprint,
    compute_conservative_rating,
    load_state,
)
from tie_detector import detect_ties, summarize_ties
from tournament_config import (
    STATE_FILE,
    TIEBREAK_FILE,
    TIEBREAK_MAX_ROUNDS,
    TIEBREAK_SCORE_PRECISION,
    TS_MU,
    TS_SIGMA,
    trueskill_env,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _empty_temp_state(players: List[str]) -> Dict[str, Any]:
    ratings = {player: {"mu": TS_MU, "sigma": TS_SIGMA} for player in players}
    records = {
        player: {"wins": 0, "losses": 0, "draws": 0}
        for player in players
    }
    return {"ratings": ratings, "records": records, "match_history": []}


def _rating_from_state(state: Dict[str, Any], player_id: str):
    rating = state["ratings"][player_id]
    return trueskill_env.create_rating(mu=rating["mu"], sigma=rating["sigma"])


def _apply_result(
    temp_state: Dict[str, Any],
    round_num: int,
    match_id: str,
    white: str,
    black: str,
    winner: Optional[str],
) -> None:
    wr = _rating_from_state(temp_state, white)
    br = _rating_from_state(temp_state, black)

    if winner == "white":
        nw, nb = trueskill_env.rate_1vs1(wr, br)
        temp_state["records"][white]["wins"] += 1
        temp_state["records"][black]["losses"] += 1
    elif winner == "black":
        nb, nw = trueskill_env.rate_1vs1(br, wr)
        temp_state["records"][black]["wins"] += 1
        temp_state["records"][white]["losses"] += 1
    else:
        nw, nb = trueskill_env.rate_1vs1(wr, br, drawn=True)
        temp_state["records"][white]["draws"] += 1
        temp_state["records"][black]["draws"] += 1

    temp_state["ratings"][white] = {"mu": nw.mu, "sigma": nw.sigma}
    temp_state["ratings"][black] = {"mu": nb.mu, "sigma": nb.sigma}
    temp_state["match_history"].append(
        {
            "match_id": match_id,
            "white": white,
            "black": black,
            "winner": winner,
            "round": round_num,
        }
    )


def _run_group_round(
    group_players: List[str],
    temp_state: Dict[str, Any],
    round_num: int,
) -> List[str]:
    errors: List[str] = []
    matches = generate_tiebreaker_matchups(group_players, temp_state, round_num)

    for match in matches:
        white = match["white"]
        black = match["black"]
        if black is None:
            continue

        white_eval, black_eval, error = load_eval_functions(white, black)
        if error:
            logger.warning("Tiebreak load failed for %s vs %s: %s", white, black, error)
            errors.append(error)
            _apply_result(temp_state, round_num, match["match_id"], white, black, None)
            continue

        result, error = run_match(white, black, white_eval, black_eval)
        if error:
            logger.warning("Tiebreak match failed for %s vs %s: %s", white, black, error)
            errors.append(error)
            _apply_result(temp_state, round_num, match["match_id"], white, black, None)
            continue

        winner = result.get("winner") if isinstance(result, dict) else None
        _apply_result(temp_state, round_num, match["match_id"], white, black, winner)

    return errors


def _group_rankings(temp_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    rankings = []
    for submission_id, rating in temp_state["ratings"].items():
        mu = float(rating["mu"])
        sigma = float(rating["sigma"])
        rankings.append(
            {
                "submission_id": submission_id,
                "mu": mu,
                "sigma": sigma,
                "score": compute_conservative_rating(mu, sigma),
                "record": temp_state["records"].get(
                    submission_id, {"wins": 0, "losses": 0, "draws": 0}
                ),
            }
        )

    rankings.sort(
        key=lambda item: (-item["score"], -item["mu"], str(item["submission_id"]))
    )

    for rank, entry in enumerate(rankings, start=1):
        entry["rank"] = rank
    return rankings


def run_tiebreakers(
    state_file: str = STATE_FILE,
    output_file: str = TIEBREAK_FILE,
    max_rounds: int = TIEBREAK_MAX_ROUNDS,
    precision: int = TIEBREAK_SCORE_PRECISION,
) -> Dict[str, Any]:
    logger.info("Running temporary tiebreakers from %s", state_file)
    state = load_state(state_file)
    tied_groups = detect_ties(state, precision=precision)

    result: Dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "score_precision": precision,
        "state_fingerprint": build_tiebreak_fingerprint(state, precision),
        "groups": [],
        "rankings": {},
    }

    if not tied_groups:
        logger.info("No tied groups found for temporary tiebreaking")
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
        return result

    logger.info("\n%s", summarize_ties(state, tied_groups))

    for group_index, group_players in enumerate(tied_groups, start=1):
        temp_state = _empty_temp_state(group_players)
        errors: List[str] = []

        for round_num in range(1, max_rounds + 1):
            errors.extend(_run_group_round(group_players, temp_state, round_num))
            remaining = detect_ties(temp_state, precision=precision)
            if not remaining:
                break

        rankings = _group_rankings(temp_state)
        main_score = compute_conservative_rating(
            state["ratings"][group_players[0]]["mu"],
            state["ratings"][group_players[0]]["sigma"],
        )
        group_result = {
            "group_index": group_index,
            "main_score": main_score,
            "players": list(group_players),
            "rankings": rankings,
            "errors": errors,
        }
        result["groups"].append(group_result)
        for entry in rankings:
            result["rankings"][entry["submission_id"]] = {
                "group_index": group_index,
                "main_score": main_score,
                "score": entry["score"],
                "rank": entry["rank"],
                "mu": entry["mu"],
                "sigma": entry["sigma"],
            }

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run temporary tiebreak tournaments for equal-score groups"
    )
    parser.add_argument("--state", type=str, default=STATE_FILE)
    parser.add_argument("--output", type=str, default=TIEBREAK_FILE)
    parser.add_argument("--max-rounds", type=int, default=TIEBREAK_MAX_ROUNDS)
    parser.add_argument("--precision", type=int, default=TIEBREAK_SCORE_PRECISION)
    args = parser.parse_args()

    result = run_tiebreakers(
        state_file=args.state,
        output_file=args.output,
        max_rounds=args.max_rounds,
        precision=args.precision,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
