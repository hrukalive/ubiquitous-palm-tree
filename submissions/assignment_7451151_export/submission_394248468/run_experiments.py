import json

from breakthrough import offensive_eval_1, offensive_eval_2
from breakthrough import defensive_eval_1, defensive_eval_2
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
# YOUR NAME: Adeel Syed
# YOUR WPI ID: 901034262
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
    print("1. Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = MinimaxAgent("White-Offensive1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("Black-Offensive1", depth=3, eval_fn=offensive_eval_1)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))

    print("2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)")
    white_agent = AlphaBetaAgent("White-Offensive2", depth=4, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("Black-Defensive1", depth=4, eval_fn=defensive_eval_1)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))

    print("3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = AlphaBetaAgent("White-Defensive2", depth=4, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("Black-Offensive1", depth=4, eval_fn=offensive_eval_1)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))

    print("4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)")
    white_agent = AlphaBetaAgent("White-Offensive2", depth=4, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("Black-Offensive1", depth=4, eval_fn=offensive_eval_1)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))

    print("5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)")
    white_agent = AlphaBetaAgent("White-Defensive2", depth=4, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("Black-Defensive1", depth=4, eval_fn=defensive_eval_1)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))

    print("6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)")
    white_agent = AlphaBetaAgent("White-Offensive2", depth=4, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("Black-Defensive2", depth=4, eval_fn=defensive_eval_2)

    result = play_game(white_agent, black_agent, max_moves=500)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
