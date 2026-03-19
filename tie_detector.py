"""
Detect groups of submissions that share the same main leaderboard score.
"""

import argparse
import json
from collections import defaultdict
from typing import Dict, List, Tuple


def _score_from_rating(rating: Dict[str, float]) -> float:
    mu = float(rating.get("mu", 25.0))
    sigma = float(rating.get("sigma", 8.333))
    return mu - 3 * sigma


def detect_ties(state: Dict, precision: int = 6) -> List[List[str]]:
    """
    Group players by rounded conservative score (mu - 3*sigma).
    """
    score_groups = defaultdict(list)
    ratings = state.get("ratings", {})

    for player_id, rating in ratings.items():
        if not isinstance(rating, dict):
            continue
        score_groups[round(_score_from_rating(rating), precision)].append(player_id)

    tied_groups = [players for players in score_groups.values() if len(players) >= 2]

    def sort_key(group: List[str]) -> Tuple[float, int]:
        score = _score_from_rating(ratings[group[0]])
        return (-score, -len(group))

    tied_groups.sort(key=sort_key)
    return tied_groups


def summarize_ties(state: Dict, tied_groups: List[List[str]]) -> str:
    if not tied_groups:
        return "No tied groups found. All main scores are unique."

    lines = []
    total_tied_players = sum(len(group) for group in tied_groups)
    lines.append(
        f"Found {len(tied_groups)} tied groups involving {total_tied_players} submissions:\n"
    )

    for idx, group in enumerate(tied_groups, start=1):
        score = _score_from_rating(state["ratings"][group[0]])
        lines.append(f"Tie Group {idx}: {len(group)} submissions at score={score:.6f}")
        for player_id in sorted(group):
            rating = state["ratings"][player_id]
            record = state.get("records", {}).get(
                player_id, {"wins": 0, "losses": 0, "draws": 0}
            )
            lines.append(
                f"  - {player_id} (mu={rating['mu']:.3f}, sigma={rating['sigma']:.3f}, "
                f"{record['wins']}-{record['losses']}-{record['draws']})"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Detect tied main scores in tournament state"
    )
    parser.add_argument(
        "--state",
        type=str,
        default="tournament_state.json",
        help="Path to tournament state file",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=6,
        help="Decimal places used to compare main scores",
    )
    args = parser.parse_args()

    try:
        with open(args.state, "r", encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        print(f"Error: State file not found: {args.state}")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in state file: {args.state}")
        return 1

    tied_groups = detect_ties(state, precision=args.precision)
    print(summarize_ties(state, tied_groups))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
