import json

from breakthrough import defensive_eval_1, offensive_eval_1
from breakthrough import defensive_eval_2, offensive_eval_2
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
# YOUR NAME: Patrick Tirch
# YOUR WPI ID: 901008117
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

    # 1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
    # w_agent = MinimaxAgent("Minimax Off 1", 2, eval_fn=offensive_eval_1)
    # b_agent = AlphaBetaAgent("AlphaBeta Off 1", 2, eval_fn=offensive_eval_1)
    # result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    # 2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    # w_agent = AlphaBetaAgent("AlphaBeta Off 2", 2, eval_fn=offensive_eval_2)
    # b_agent = AlphaBetaAgent("AlphaBeta Def 1", 2, eval_fn=defensive_eval_1)
    # result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    # 3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    # w_agent = AlphaBetaAgent("AlphaBeta Def 2", 2, eval_fn=defensive_eval_1)
    # b_agent = AlphaBetaAgent("AlphaBeta Off 1", 2, eval_fn=offensive_eval_1)
    # result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    # 4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    # w_agent = AlphaBetaAgent("AlphaBeta Off 2", 2, eval_fn=offensive_eval_2)
    # b_agent = AlphaBetaAgent("AlphaBeta Off 1", 2, eval_fn=offensive_eval_1)
    # result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    # 5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    # w_agent = AlphaBetaAgent("AlphaBeta Def 2", 2, eval_fn=defensive_eval_2)
    # b_agent = AlphaBetaAgent("AlphaBeta Def 1", 2, eval_fn=defensive_eval_1)
    # result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    # 6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
    w_agent = AlphaBetaAgent("AlphaBeta Off 2", 2, eval_fn=offensive_eval_2)
    b_agent = AlphaBetaAgent("AlphaBeta Def 2", 2, eval_fn=defensive_eval_2)
    result = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)

    print(result)

if __name__ == '__main__':
    main()
