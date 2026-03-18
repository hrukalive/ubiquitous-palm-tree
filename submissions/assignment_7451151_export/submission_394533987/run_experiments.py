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
# YOUR NAME: Beruh Zelleke
# YOUR WPI ID: 835362710
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

def run_matchup(label, white_agent, black_agent):
    print(f"\n{'='*60}")
    print(f"  Matchup: {label}")
    print(f"  White: {white_agent.name}  |  Black: {black_agent.name}")
    print(f"{'='*60}")
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(f"  Winner: {results['winner']}")
    print(f"  Total moves: {results['total_moves']}")
    print(f"  White nodes (total): {results['white_nodes']}")
    print(f"  Black nodes (total): {results['black_nodes']}")
    print(f"  White nodes/move: {results['white_nodes_per_move']:.1f}")
    print(f"  Black nodes/move: {results['black_nodes_per_move']:.1f}")
    print(f"  White time/move: {results['white_time_per_move']:.4f}s")
    print(f"  Black time/move: {results['black_time_per_move']:.4f}s")
    print(f"  White captures: {results['white_captures']}")
    print(f"  Black captures: {results['black_captures']}")
    return results


def main():
    matchups = [
        # Required matchups
        ("1) Minimax(Off1) vs AlphaBeta(Off1)",
         MinimaxAgent("Minimax Off1", depth=2, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)),
        ("2) AlphaBeta(Off2) vs AlphaBeta(Def1)",
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)),
        ("3) AlphaBeta(Def2) vs AlphaBeta(Off1)",
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)),
        ("4) AlphaBeta(Off2) vs AlphaBeta(Off1)",
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)),
        ("5) AlphaBeta(Def2) vs AlphaBeta(Def1)",
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)),
        ("6) AlphaBeta(Off2) vs AlphaBeta(Def2)",
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)),
        # Swapped colors (testing first move advantage)
        ("1R) AlphaBeta(Off1) vs Minimax(Off1)",
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
         MinimaxAgent("Minimax Off1", depth=2, eval_fn=offensive_eval_1)),
        ("2R) AlphaBeta(Def1) vs AlphaBeta(Off2)",
         AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)),
        ("3R) AlphaBeta(Off1) vs AlphaBeta(Def2)",
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)),
        ("4R) AlphaBeta(Off1) vs AlphaBeta(Off2)",
         AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)),
        ("5R) AlphaBeta(Def1) vs AlphaBeta(Def2)",
         AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)),
        ("6R) AlphaBeta(Def2) vs AlphaBeta(Off2)",
         AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)),
    ]

    all_results = []
    for label, white, black in matchups:
        result = run_matchup(label, white, black)
        all_results.append({"matchup": label, **result})

    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    for r in all_results:
        print(f"  {r['matchup']}: winner={r['winner']}, moves={r['total_moves']}, "
              f"W_captures={r['white_captures']}, B_captures={r['black_captures']}")

    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nResults saved to experiment_results.json")


if __name__ == '__main__':
    main()
