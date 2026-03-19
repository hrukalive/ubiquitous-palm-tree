"""
TrueSkill-informed Swiss pairing system for Breakthrough tournament.
Generates match schedules for each round with quality-optimized pairings.
"""

import json
import os
import random
import argparse
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, cast

from tournament_config import (
    RESULTS_DIR,
    STATE_FILE,
    GAMES_PER_PAIRING,
    REPEAT_WINDOW,
    TOURNAMENT_SEED,
    trueskill_env,
)


logger = logging.getLogger(__name__)


def load_tournament_state(state_file: str = STATE_FILE) -> Dict[str, Any]:
    """
    Load tournament state from JSON file.
    If file doesn't exist, initialize with default ratings for all players.
    """
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    else:
        # Initialize empty state
        return {"ratings": {}, "match_history": []}


def get_all_player_ids(state: Dict[str, Any]) -> List[str]:
    """Extract all unique player IDs from state."""
    ratings = cast(Dict[str, Dict[str, Any]], state.get("ratings", {}))
    player_ids = set(ratings.keys())

    # Also add players from match history who might not have ratings yet
    match_history = cast(List[Dict[str, Any]], state.get("match_history", []))
    for match in match_history:
        white = match.get("white")
        black = match.get("black")
        if isinstance(white, str):
            player_ids.add(white)
        if isinstance(black, str):
            player_ids.add(black)

    return sorted(list(player_ids))


def get_player_rating(player_id: str, state: Dict[str, Any]):
    """Get TrueSkill rating for a player, or create default if not exists."""
    ratings = cast(Dict[str, Dict[str, Any]], state.get("ratings", {}))
    if player_id in ratings:
        mu = ratings[player_id].get("mu")
        sigma = ratings[player_id].get("sigma")
        return trueskill_env.create_rating(mu=mu, sigma=sigma)
    else:
        return trueskill_env.create_rating()


def conservative_rating(rating):
    """Calculate conservative rating: mu - 3*sigma"""
    return rating.mu - 3 * rating.sigma


def was_paired_recently(
    player1: str,
    player2: str,
    repeat_window: int,
    match_history: List[Dict[str, Any]],
    current_round: int,
) -> bool:
    """
    Check if two players have faced each other within repeat_window rounds.
    """
    for match in match_history:
        # Check if they played (in any color order)
        if (match.get("white") == player1 and match.get("black") == player2) or (
            match.get("white") == player2 and match.get("black") == player1
        ):
            match_round = cast(int, match.get("round", 0))
            if current_round - match_round <= repeat_window:
                return True
    return False


def generate_matchups(
    round_num: int,
    state_file: str = STATE_FILE,
    seed: Optional[int] = None,
    student_map: Optional[Dict[str, str]] = None,
    retired: Optional[Set[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate match-ups for a given round using Swiss pairing algorithm.

    Args:
        round_num: The round number to generate matches for
        state_file: Path to tournament state JSON file
        seed: Optional seed override (defaults to round_num * 1000 + TOURNAMENT_SEED)
        student_map: Optional mapping from submission ID to student ID
        retired: Optional set of retired submission IDs to exclude

    Returns:
        List of match dictionaries with structure:
        {"match_id": str, "white": str, "black": str, "round": int}
    """
    # Load state
    state = load_tournament_state(state_file)
    match_history = cast(List[Dict[str, Any]], state.get("match_history", []))

    # Get all players
    all_players = get_all_player_ids(state)
    players = list(all_players)

    # Filter out retired submissions
    if retired:
        players = [p for p in players if p not in retired]
        logger.info(
            f"Filtered out {len(set(all_players) - set(players))} retired submissions"
        )

    if not players:
        raise ValueError("No players found in tournament state")

    # Set random seed for reproducibility
    if seed is None:
        seed = round_num * 1000 + TOURNAMENT_SEED
    random.seed(seed)

    # Load ratings and create (player, rating) tuples
    player_ratings = []
    for player_id in players:
        rating = get_player_rating(player_id, state)
        player_ratings.append((player_id, rating))

    # Sort by conservative rating (descending)
    player_ratings.sort(key=lambda x: conservative_rating(x[1]), reverse=True)
    sorted_players = [p[0] for p in player_ratings]
    ratings_dict = {p[0]: p[1] for p in player_ratings}

    # Swiss pairing algorithm
    paired = set()
    matches = []
    match_id_counter = 1

    for i, player1 in enumerate(sorted_players):
        if player1 in paired:
            continue

        best_opponent = None
        best_quality = -1

        # Try to find best unpaired opponent (respecting repeat window)
        for j in range(i + 1, len(sorted_players)):
            player2 = sorted_players[j]
            if player2 in paired:
                continue

            # Check same-student constraint
            if student_map:
                sid1 = student_map.get(player1, "")
                sid2 = student_map.get(player2, "")
                if sid1 and sid2 and sid1 == sid2:
                    logger.debug(
                        f"Skipping same-student pairing: {player1} vs {player2}"
                    )
                    continue

            # Check repeat window constraint
            if was_paired_recently(
                player1, player2, REPEAT_WINDOW, match_history, round_num
            ):
                continue

            # Calculate match quality
            quality = getattr(trueskill_env, "quality_1vs1")(
                ratings_dict[player1], ratings_dict[player2]
            )
            if quality > best_quality:
                best_quality = quality
                best_opponent = player2

        # If no valid opponent found (all in repeat window), relax constraint
        if best_opponent is None:
            for j in range(i + 1, len(sorted_players)):
                player2 = sorted_players[j]
                if player2 in paired:
                    continue

                # Check same-student even in fallback
                if student_map:
                    sid1 = student_map.get(player1, "")
                    sid2 = student_map.get(player2, "")
                    if sid1 and sid2 and sid1 == sid2:
                        logger.debug(
                            f"Skipping same-student fallback pairing: {player1} vs {player2}"
                        )
                        continue

                best_opponent = player2
                break

        # Create matches if opponent found
        if best_opponent is not None:
            paired.add(player1)
            paired.add(best_opponent)

            # Generate GAMES_PER_PAIRING games (swap colors if GAMES_PER_PAIRING == 2)
            for game_num in range(GAMES_PER_PAIRING):
                match_id = f"r{round_num:02d}_match_{match_id_counter:04d}"
                match_id_counter += 1

                if game_num == 0:
                    white, black = player1, best_opponent
                else:
                    white, black = best_opponent, player1

                matches.append(
                    {
                        "match_id": match_id,
                        "white": white,
                        "black": black,
                        "round": round_num,
                    }
                )

    # Handle odd player count (bye system)
    bye_player = None
    for player in sorted_players:
        if player not in paired:
            bye_player = player
            break

    if bye_player is not None:
        match_id = f"r{round_num:02d}_match_{match_id_counter:04d}"
        matches.append(
            {
                "match_id": match_id,
                "white": bye_player,
                "black": None,  # None indicates bye
                "round": round_num,
            }
        )

    return matches


def generate_tiebreaker_matchups(
    players: List[str],
    state: Dict[str, Any],
    round_num: int,
    match_id_offset: int = 0,
    seed: Optional[int] = None,
    student_map: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate no-bye matchups for a tiebreaker group.

    Small groups use a complete round-robin schedule so every pair is evaluated.
    Larger groups use Swiss-style pairing with one extra series for odd-sized
    groups so nobody sits out.

    Args:
        players: List of player IDs in the tied group (2-4 players)
        state: Tournament state dict with ratings and match_history
        round_num: Tiebreaker round number (100+)
        match_id_offset: Starting offset for match IDs (for multiple groups)
        seed: Random seed for reproducibility (optional)

    Returns:
        List of match dicts with format:
        {"match_id": "r100_match_0001", "white": str, "black": str, "round": int}

    Example:
        >>> players = ["sub1", "sub2", "sub3"]
        >>> generate_tiebreaker_matchups(players, state, 100, 0, seed=42)
        [{"match_id": "r100_match_0001", "white": "sub1", "black": "sub2", "round": 100},
         {"match_id": "r100_match_0002", "white": "sub2", "black": "sub1", "round": 100},
         {"match_id": "r100_match_0003", "white": "sub1", "black": "sub3", "round": 100},
         ...]
    """
    if len(players) < 2:
        raise ValueError(f"Need at least 2 players for tiebreaker, got {len(players)}")

    # Set random seed if provided
    if seed is not None:
        random.seed(seed)

    # Get ratings for all players
    player_ratings = {}
    for player_id in players:
        player_ratings[player_id] = get_player_rating(player_id, state)

    # Sort by conservative rating (mu - 3*sigma)
    def conservative_rating(player_id: str) -> float:
        rating = player_ratings[player_id]
        return rating.mu - 3 * rating.sigma

    sorted_players = sorted(players, key=conservative_rating, reverse=True)

    # Check for recent matchups within this tiebreaker iteration
    # (avoid immediate rematches within same tiebreaker round)
    recent_matches = set()
    match_history = cast(List[Dict[str, Any]], state.get("match_history", []))
    for match in match_history:
        if match.get("round") == round_num:  # Same tiebreaker round
            white = match.get("white")
            black = match.get("black")
            if white and black:
                recent_matches.add(tuple(sorted([white, black])))

    def can_pair(player1: str, player2: str) -> bool:
        if player1 == player2:
            return False
        if student_map:
            sid1 = student_map.get(player1, "")
            sid2 = student_map.get(player2, "")
            if sid1 and sid2 and sid1 == sid2:
                return False
        return True

    def add_series(
        match_list: List[Dict[str, Any]],
        counter: int,
        player1: str,
        player2: str,
    ) -> int:
        for game_num in range(GAMES_PER_PAIRING):
            counter += 1
            match_id = f"r{round_num}_match_{counter:04d}"
            if game_num % 2 == 0:
                white, black = player1, player2
            else:
                white, black = player2, player1
            match_list.append(
                {
                    "match_id": match_id,
                    "white": white,
                    "black": black,
                    "round": round_num,
                }
            )
        return counter

    # Very small tied groups benefit more from complete coverage than Swiss pairing.
    if len(sorted_players) <= 4:
        matches = []
        match_id_counter = match_id_offset
        for i, player1 in enumerate(sorted_players):
            for player2 in sorted_players[i + 1 :]:
                if not can_pair(player1, player2):
                    continue
                match_id_counter = add_series(
                    matches, match_id_counter, player1, player2
                )
        return matches

    # Generate pairings for larger groups.
    matches = []
    paired = set()
    match_id_counter = match_id_offset

    # Pair players sequentially with quality checks
    for i, player1 in enumerate(sorted_players):
        if player1 in paired:
            continue

        # Find best opponent from remaining players
        best_opponent = None
        best_quality = -1.0

        for player2 in sorted_players[i + 1 :]:
            if player2 in paired:
                continue

            if not can_pair(player1, player2):
                logger.debug(
                    f"Skipping same-student tiebreaker pairing: {player1} vs {player2}"
                )
                continue

            # Check if already played recently
            pairing_key = tuple(sorted([player1, player2]))
            if pairing_key in recent_matches:
                continue  # Skip recent rematches

            # Calculate match quality
            quality = getattr(trueskill_env, "quality_1vs1")(
                player_ratings[player1], player_ratings[player2]
            )

            if quality > best_quality:
                best_quality = quality
                best_opponent = player2

        # If no valid opponent found (all recent), pair anyway with closest rating
        if best_opponent is None:
            for player2 in sorted_players[i + 1 :]:
                if player2 in paired:
                    continue

                if not can_pair(player1, player2):
                    logger.debug(
                        f"Skipping same-student tiebreaker fallback: {player1} vs {player2}"
                    )
                    continue

                best_opponent = player2
                break

        if best_opponent is not None:
            paired.add(player1)
            paired.add(best_opponent)
            match_id_counter = add_series(
                matches, match_id_counter, player1, best_opponent
            )

    # Odd-sized groups: give the remaining player an extra series instead of a bye.
    remaining_players = [player for player in sorted_players if player not in paired]
    if remaining_players:
        extra_player = remaining_players[0]
        best_opponent = None
        best_quality = -1.0
        for opponent in sorted_players:
            if not can_pair(extra_player, opponent):
                continue
            quality = getattr(trueskill_env, "quality_1vs1")(
                player_ratings[extra_player], player_ratings[opponent]
            )
            if quality > best_quality:
                best_quality = quality
                best_opponent = opponent
        if best_opponent is None:
            raise ValueError(
                f"Could not find an extra opponent for odd tiebreak group: {extra_player}"
            )
        match_id_counter = add_series(
            matches, match_id_counter, extra_player, best_opponent
        )

    return matches


def write_matches_to_file(
    round_num: int, matches: List[Dict[str, Any]], results_dir: str = RESULTS_DIR
) -> str:
    """
    Write matches to results/round_XX/matches.json

    Args:
        round_num: Round number
        matches: List of match dictionaries
        results_dir: Results directory base path

    Returns:
        Path to the written file
    """
    round_dir = Path(results_dir) / f"round_{round_num:02d}"
    round_dir.mkdir(parents=True, exist_ok=True)

    output_file = round_dir / "matches.json"
    with open(output_file, "w") as f:
        json.dump(matches, f, indent=2)

    return str(output_file)


def main():
    """CLI interface for matchmaker"""
    parser = argparse.ArgumentParser(
        description="Generate TrueSkill-informed Swiss pairings for a tournament round"
    )
    parser.add_argument(
        "--round",
        type=int,
        required=True,
        help="Round number to generate matches for",
    )
    parser.add_argument(
        "--state",
        type=str,
        default=STATE_FILE,
        help=f"Path to tournament state file (default: {STATE_FILE})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: round_num * 1000 + TOURNAMENT_SEED)",
    )

    args = parser.parse_args()

    # Generate matchups
    matches = generate_matchups(args.round, args.state, args.seed)

    # Write to file
    output_file = write_matches_to_file(args.round, matches)

    # Print summary
    print(f"Generated {len(matches)} matches for round {args.round}")
    print(f"Output written to: {output_file}")
    print(f"\nFirst 5 matches:")
    for match in matches[:5]:
        if match.get("black"):
            print(
                f"  {match['match_id']}: {match['white']} (white) vs {match['black']} (black)"
            )
        else:
            print(f"  {match['match_id']}: {match['white']} (white) [BYE]")


if __name__ == "__main__":
    main()
