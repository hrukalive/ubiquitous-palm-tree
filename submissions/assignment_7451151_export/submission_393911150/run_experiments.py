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
# YOUR NAME: Vu Nguyen
# YOUR WPI ID: 902022654
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
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
    ...  # YOUR EXPERIMENTS HERE
    matchups = [
        ("Minimax Off1 vs AlphaBeta Off1",
         MinimaxAgent("Minimax Off1", 3, offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off1", 4, offensive_eval_1)),

        ("AlphaBeta Off2 vs AlphaBeta Def1",
         AlphaBetaAgent("AlphaBeta Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", 4, defensive_eval_1)),

        ("AlphaBeta Def2 vs AlphaBeta Off1",
         AlphaBetaAgent("AlphaBeta Def2", 4, defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", 4, offensive_eval_1)),

        ("AlphaBeta Off2 vs AlphaBeta Off1",
         AlphaBetaAgent("AlphaBeta Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", 4, offensive_eval_1)),

        ("AlphaBeta Def2 vs AlphaBeta Def1",
         AlphaBetaAgent("AlphaBeta Def2", 4, defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", 4, defensive_eval_1)),

        ("AlphaBeta Off2 vs AlphaBeta Def2",
         AlphaBetaAgent("AlphaBeta Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def2", 4, defensive_eval_2)),
    ]

    for title, white_agent, black_agent in matchups:
        print("\n====================================================")
        print(title)
        print("====================================================")

        white_agent.reset()
        black_agent.reset()

        results = play_game(
            white_agent,
            black_agent,
            max_moves=400,
            display=False,
            progress=True
        )

        print("\nWinner:", results["winner"])
        print("Total moves:", results["total_moves"])

        print("\n--- Nodes ---")
        print("White total nodes:", results["white_nodes"])
        print("Black total nodes:", results["black_nodes"])

        print("White avg nodes per move:", results["white_nodes_per_move"])
        print("Black avg nodes per move:", results["black_nodes_per_move"])

        print("White avg time per move:", results["white_time_per_move"])
        print("Black avg time per move:", results["black_time_per_move"])

        print("\n--- Captures ---")
        print("White captured:", results["white_captures"])
        print("Black captured:", results["black_captures"])

        print("====================================================\n")


if __name__ == '__main__':
    main()
