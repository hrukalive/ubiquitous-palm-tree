import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2, defensive_eval_test
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
from src.games import Game
from breakthrough import Breakthrough


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Zhiyan Jiang
# YOUR WPI ID: jzhiyan@wpi.edu
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
    game = Breakthrough()
    # white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    # black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_2)

    white_agent = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_test)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_test)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(f"Experiment 1: {results}")

    # white_agent = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=offensive_eval_2)
    # black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=defensive_eval_1)
    # results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    # print(f"Experiment 2: {results}")


if __name__ == '__main__':
    main()
