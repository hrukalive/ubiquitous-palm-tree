import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Meray Khela
# YOUR WPI ID: 997073788
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
# Perform the necessary experiments here to generate data required by the report.

def run_matchup(white_agent, black_agent, matchup_num, description):
    """Run one game between two agents and print the results."""
    print(f"\n{'=' * 60}")
    print(f"Matchup {matchup_num}: {description}")
    print(f"  WHITE: {white_agent.name}  |  BLACK: {black_agent.name}")
    print("=" * 60)

    # Play the full game and collect stats (nodes visited, time per move, etc.)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)

    # Print who won and how long the game lasted
    print(f"\nWinner: {results['winner'].upper() if results['winner'] else 'DRAW (max moves)'}")
    print(f"Total moves: {results['total_moves']}")

    # Print stats for the WHITE player
    print(f"\nWHITE ({results['white_name']}):")
    print(f"  Total nodes expanded:     {results['white_nodes']}")
    print(f"  Avg nodes/move:           {results['white_nodes_per_move']:.1f}")
    print(f"  Avg time/move (s):        {results['white_time_per_move']:.4f}")
    print(f"  Opponent pieces captured: {results['white_captures']}")

    # Print stats for the BLACK player
    print(f"\nBLACK ({results['black_name']}):")
    print(f"  Total nodes expanded:     {results['black_nodes']}")
    print(f"  Avg nodes/move:           {results['black_nodes_per_move']:.1f}")
    print(f"  Avg time/move (s):        {results['black_time_per_move']:.4f}")
    print(f"  Opponent pieces captured: {results['black_captures']}")

    # Return the stats dict so we can save everything to a file later
    return results


def main():
    all_results = []  # we'll store the results from every matchup here

    # ------------------------------------------------------------------
    # Matchup 1: Minimax (Offensive Eval 1) vs Alpha-beta (Offensive Eval 1)
    # Both agents use the exact same scoring function, so the only difference
    # is that alpha-beta can look deeper because it skips useless branches.
    # ------------------------------------------------------------------
    white = MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black, 1, "Minimax (Off1) vs Alpha-beta (Off1)"))

    # ------------------------------------------------------------------
    # Matchup 2: Alpha-beta (Offensive Eval 2) vs Alpha-beta (Defensive Eval 1)
    # Can our improved offensive strategy beat the basic defensive strategy?
    # ------------------------------------------------------------------
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    all_results.append(run_matchup(white, black, 2, "AlphaBeta (Off2) vs AlphaBeta (Def1)"))

    # ------------------------------------------------------------------
    # Matchup 3: Alpha-beta (Defensive Eval 2) vs Alpha-beta (Offensive Eval 1)
    # Can our improved defensive strategy beat the basic offensive strategy?
    # ------------------------------------------------------------------
    white = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black, 3, "AlphaBeta (Def2) vs AlphaBeta (Off1)"))

    # ------------------------------------------------------------------
    # Matchup 4: Alpha-beta (Offensive Eval 2) vs Alpha-beta (Offensive Eval 1)
    # Does Offensive Eval 2 actually beat the older Offensive Eval 1?
    # ------------------------------------------------------------------
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black, 4, "AlphaBeta (Off2) vs AlphaBeta (Off1)"))

    # ------------------------------------------------------------------
    # Matchup 5: Alpha-beta (Defensive Eval 2) vs Alpha-beta (Defensive Eval 1)
    # Does Defensive Eval 2 actually beat the older Defensive Eval 1?
    # ------------------------------------------------------------------
    white = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    all_results.append(run_matchup(white, black, 5, "AlphaBeta (Def2) vs AlphaBeta (Def1)"))

    # ------------------------------------------------------------------
    # Matchup 6: Alpha-beta (Offensive Eval 2) vs Alpha-beta (Defensive Eval 2)
    # Our best offensive strategy vs our best defensive strategy — who wins?
    # ------------------------------------------------------------------
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    all_results.append(run_matchup(white, black, 6, "AlphaBeta (Off2) vs AlphaBeta (Def2)"))

    # Save every matchup's data to a JSON file so we can reference it in the report
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\n\nAll results saved to experiment_results.json")

    # Print a quick one-line summary of every matchup so results are easy to scan
    print("\n\n" + "=" * 60)
    print("SUMMARY OF RESULTS")
    print("=" * 60)
    for i, r in enumerate(all_results, 1):
        winner_str = r["winner"].upper() if r["winner"] else "DRAW"
        print(f"Matchup {i}: {r['white_name']} vs {r['black_name']} -> Winner: {winner_str} in {r['total_moves']} moves")


if __name__ == '__main__':
    main()