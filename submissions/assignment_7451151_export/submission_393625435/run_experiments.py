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
# YOUR NAME: Pranav Santhosh
# YOUR WPI ID: 997075093
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

def main():
    max_moves = 400
    display = False
    progress = True

    matchups = [
        (
            "1) Minimax (Off1) vs AlphaBeta (Off1)",
            MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        ),
        (
            "2) AlphaBeta (Off2) vs AlphaBeta (Def1)",
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        ),
        (
            "3) AlphaBeta (Def2) vs AlphaBeta (Off1)",
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        ),
        (
            "4) AlphaBeta (Off2) vs AlphaBeta (Off1)",
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        ),
        (
            "5) AlphaBeta (Def2) vs AlphaBeta (Def1)",
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        ),
        (
            "6) AlphaBeta (Off2) vs AlphaBeta (Def2)",
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        ),
    ]

    all_results = []

    for title, white_agent, black_agent in matchups:
        white_agent.reset()
        black_agent.reset()

        print("\n" + "=" * 78)
        print(title)
        print("=" * 78)

        result = play_game(
            white_agent,
            black_agent,
            max_moves=max_moves,
            display=display,
            progress=progress
        )

        all_results.append({
            "matchup": title,
            **result
        })

        print("Winner:", result["winner"])
        print("Total moves:", result["total_moves"])
        print("White nodes:", result["white_nodes"], "Black nodes:", result["black_nodes"])
        print("White nodes/move:", result["white_nodes_per_move"], "Black nodes/move:", result["black_nodes_per_move"])
        print("White time/move:", result["white_time_per_move"], "Black time/move:", result["black_time_per_move"])
        print("White captures:", result["white_captures"], "Black captures:", result["black_captures"])

    with open("ip2_experiments.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\nSaved results to ip2_experiments.json")


if __name__ == '__main__':
    main()