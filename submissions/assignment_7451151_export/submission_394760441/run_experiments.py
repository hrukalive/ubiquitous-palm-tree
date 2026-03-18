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
# YOUR NAME: Jack Trask
# YOUR WPI ID: 901015154
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm



# Perform the necessary experiments here to generate data required by the report.

def main():
    experiments = [
        # 1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
        {
            "name": "Minimax Off1 vs AlphaBeta Off1",
            "white": MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },

        # 2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        {
            "name": "AlphaBeta Off2 vs AlphaBeta Def1",
            "white": AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        },

        # 3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        {
            "name": "AlphaBeta Def2 vs AlphaBeta Off1",
            "white": AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },

        # 4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        {
            "name": "AlphaBeta Off2 vs AlphaBeta Off1",
            "white": AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },

        # 5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        {
            "name": "AlphaBeta Def2 vs AlphaBeta Def1",
            "white": AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        },

        # 6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
        {
            "name": "AlphaBeta Off2 vs AlphaBeta Def2",
            "white": AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        },
    ]

    results = []

    for i, exp in enumerate(experiments, start=1):
        print(f"\n=== Experiment {i}: {exp['name']} ===")
        print(f"White: {exp['white'].name}")
        print(f"Black: {exp['black'].name}")

        result = play_game(
            exp["white"],
            exp["black"],
            max_moves=400,
            display=True,
            progress=True,
        )

        result["experiment"] = exp["name"]
        results.append(result)

        print("Result:", result)

    with open("breakthrough_experiments.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nAll experiments have been executed.")
    print("Results saved to breakthrough_experiments.json")


if __name__ == '__main__':
    main()
