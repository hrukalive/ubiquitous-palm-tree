import json

from breakthrough import offensive_eval_1, defensive_eval_1, Breakthrough
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
# YOUR NAME: ???
# YOUR WPI ID: ???
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

def test(eval1, eval2):
    for _ in range(5):  # Play each matchup 5 times
        w_agent = AlphaBetaAgent("E1", 3, eval_fn=eval1)
        b_agent = AlphaBetaAgent("E2", 3, eval_fn=eval2)
        res = play_game(w_agent, b_agent, max_moves=400, progress=False)
        print(res)

    for _ in range(5):  # Play each matchup 5 times
        b_agent = AlphaBetaAgent("E1", 3, eval_fn=eval1)
        w_agent = AlphaBetaAgent("E2", 3, eval_fn=eval2)
        res = play_game(w_agent, b_agent, max_moves=400, progress=False)
        print(res)

def main():
    #
    # print("Offensive 1 vs Defensive 1")
    # test(offensive_eval_1, defensive_eval_1)
    #
    # print("Offensive 2 vs Defensive 1")
    # test(offensive_eval_2, defensive_eval_1)
    #
    # print("Offensive 1 vs Defensive 2")
    # test(offensive_eval_1, defensive_eval_2)
    #
    # print("Offensive 1 vs Offensive 2")
    # test(offensive_eval_1, offensive_eval_2)
    #
    print("Defensive 1 vs Defensive 2")
    test(defensive_eval_1, defensive_eval_2)


if __name__ == '__main__':
    main()