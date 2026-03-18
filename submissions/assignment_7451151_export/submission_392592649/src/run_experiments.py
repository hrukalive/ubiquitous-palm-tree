import json

#had to be commented out
#from breakthrough import offensive_heuristic_1, defensive_heuristic_1
#from breakthrough import offensive_heuristic_2, defensive_heuristic_2
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
# YOUR NAME: Ryan Veith
# YOUR WPI ID: 901024993
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
    # YOUR EXPERIMENTS HERE
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent, RandomAgent
    from breakthrough import Breakthrough, offensive_eval_1, offensive_eval_2, defensive_eval_1, defensive_eval_2
    game = Breakthrough()

    #1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
    print("1. Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = MinimaxAgent("Minimax Off1", depth=2, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)

    #2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    print("2. Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)")
    white_agent = MinimaxAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)

    #3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    print("3. Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = MinimaxAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)

    #4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    print("4. Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = MinimaxAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)

    #5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    print("5. Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)")
    white_agent = MinimaxAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)

    #6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
    print("6. Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)")
    white_agent = MinimaxAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)


if __name__ == '__main__':
    main()
