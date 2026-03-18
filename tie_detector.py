"""
Tie Detector - Identify groups of players with identical TrueSkill ratings.

This module groups players by rounded (mu, sigma) values to detect rating ties
in the tournament leaderboard. Used by the tiebreaker system to identify which
players need additional matches to differentiate their ratings.

Usage:
    python tie_detector.py --state tournament_state.json
"""

import json
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple


def detect_ties(state: Dict, precision: int = 2) -> List[List[str]]:
    """
    Group players by rounded (mu, sigma) values and return tied groups.

    Args:
        state: Tournament state dict with 'ratings' key
        precision: Decimal places to round mu and sigma (default: 2)

    Returns:
        List of tied groups (each group is a list of player IDs).
        Groups sorted by: largest groups first, then highest mu first.
        Only returns groups with 2+ players.

    Example:
        >>> state = {"ratings": {"p1": {"mu": 25.001, "sigma": 8.333},
        ...                      "p2": {"mu": 25.002, "sigma": 8.334}}}
        >>> detect_ties(state, precision=2)
        [['p1', 'p2']]
    """
    # Group players by (rounded_mu, rounded_sigma)
    rating_groups = defaultdict(list)

    for player_id, rating in state["ratings"].items():
        mu = rating["mu"]
        sigma = rating["sigma"]

        # Round to specified precision
        rounded_mu = round(mu, precision)
        rounded_sigma = round(sigma, precision)

        rating_key = (rounded_mu, rounded_sigma)
        rating_groups[rating_key].append(player_id)

    # Filter to groups with 2+ players (tied groups)
    tied_groups = [players for players in rating_groups.values() if len(players) >= 2]

    # Sort tied groups:
    # 1. By group size (largest first)
    # 2. By highest mu in group (descending)
    def sort_key(group: List[str]) -> Tuple[int, float]:
        group_size = len(group)
        # Get max mu from any player in group
        max_mu = max(state["ratings"][pid]["mu"] for pid in group)
        return (-group_size, -max_mu)  # Negative for descending order

    tied_groups.sort(key=sort_key)

    return tied_groups


def summarize_ties(state: Dict, tied_groups: List[List[str]]) -> str:
    """
    Generate human-readable summary of tied groups.

    Args:
        state: Tournament state dict with 'ratings' and 'records' keys
        tied_groups: List of tied groups from detect_ties()

    Returns:
        Formatted string with tie group details:
        - Group number
        - Number of players
        - Rounded (mu, sigma)
        - Conservative rating (mu - 3*sigma)
        - Player IDs with W-L-D records

    Example output:
        Tie Group 1: 3 players at (mu=35.81, sigma=5.27) conservative=20.01
          - submission_392126892 (4-0-0)
          - submission_392678463 (4-0-0)
          - submission_392898103 (4-0-0)
    """
    if not tied_groups:
        return "No tied groups found. All ratings are unique."

    lines = []
    total_tied_players = sum(len(group) for group in tied_groups)

    lines.append(
        f"Found {len(tied_groups)} tied groups involving {total_tied_players} players:\n"
    )

    for idx, group in enumerate(tied_groups, start=1):
        # Get rating from first player (all in group have same rounded rating)
        first_player = group[0]
        mu = state["ratings"][first_player]["mu"]
        sigma = state["ratings"][first_player]["sigma"]
        conservative = mu - 3 * sigma

        # Round for display
        mu_rounded = round(mu, 2)
        sigma_rounded = round(sigma, 2)
        conservative_rounded = round(conservative, 2)

        lines.append(
            f"Tie Group {idx}: {len(group)} players at "
            f"(mu={mu_rounded}, sigma={sigma_rounded}) conservative={conservative_rounded}"
        )

        # List each player with their W-L-D record
        for player_id in sorted(group):  # Sort for consistent output
            record = state["records"].get(
                player_id, {"wins": 0, "losses": 0, "draws": 0}
            )
            wins = record["wins"]
            losses = record["losses"]
            draws = record["draws"]
            lines.append(f"  - {player_id} ({wins}-{losses}-{draws})")

        lines.append("")  # Blank line between groups

    return "\n".join(lines)


def main():
    """CLI entry point for tie detection."""
    parser = argparse.ArgumentParser(
        description="Detect tied ratings in tournament state"
    )
    parser.add_argument(
        "--state",
        type=str,
        default="tournament_state.json",
        help="Path to tournament state file (default: tournament_state.json)",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=2,
        help="Decimal places to round mu and sigma (default: 2)",
    )

    args = parser.parse_args()

    # Load state
    try:
        with open(args.state, "r") as f:
            state = json.load(f)
    except FileNotFoundError:
        print(f"Error: State file not found: {args.state}")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in state file: {args.state}")
        return 1

    # Detect ties
    tied_groups = detect_ties(state, precision=args.precision)

    # Print summary
    summary = summarize_ties(state, tied_groups)
    print(summary)

    return 0


if __name__ == "__main__":
    exit(main())
