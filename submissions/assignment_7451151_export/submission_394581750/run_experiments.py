import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import Breakthrough
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

# ---------------------------------------------------------------------------
# Experiment Runner
#
# Performs the six required matchups:
# 1) Minimax Off1 vs AlphaBeta Off1
# 2) AlphaBeta Off2 vs AlphaBeta Def1
# 3) AlphaBeta Def2 vs AlphaBeta Off1
# 4) AlphaBeta Off2 vs AlphaBeta Off1
# 5) AlphaBeta Def2 vs AlphaBeta Def1
# 6) AlphaBeta Off2 vs AlphaBeta Def2
#
# For each matchup, records:
# - Winner
# - Total moves
# - Nodes expanded
# - Nodes per move
# - Time per move
# - Captures
#
# Results saved to experiment_results.json
# ---------------------------------------------------------------------------


def main():
    minimax_depth = 3
    alphabeta_depth = 4
    max_moves = 400

    matchups = [
        (
            "1) Minimax Off1 vs AlphaBeta Off1",
            MinimaxAgent("Minimax Off1", depth=minimax_depth, eval_fn=offensive_eval_1),
            AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1),
        ),
        (
            "2) AlphaBeta Off2 vs AlphaBeta Def1",
            AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1),
        ),
        (
            "3) AlphaBeta Def2 vs AlphaBeta Off1",
            AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1),
        ),
        (
            "4) AlphaBeta Off2 vs AlphaBeta Off1",
            AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1),
        ),
        (
            "5) AlphaBeta Def2 vs AlphaBeta Def1",
            AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1),
        ),
        (
            "6) AlphaBeta Off2 vs AlphaBeta Def2",
            AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2),
        ),
    ]

    all_results = []

    for label, white_agent, black_agent in matchups:
        white_agent.reset()
        black_agent.reset()

        game = Breakthrough()
        results = game.play_game(white_agent, black_agent, max_moves=max_moves)
        results["matchup"] = label
        all_results.append(results)

        print(label)
        print(json.dumps(results, indent=2))

    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("Saved results to experiment_results.json")


if __name__ == "__main__":
    main()
