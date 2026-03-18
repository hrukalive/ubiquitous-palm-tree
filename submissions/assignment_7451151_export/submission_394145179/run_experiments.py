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
# YOUR NAME: Alex Lowczyk
# YOUR WPI ID: 901009097
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
    w_agent = MinimaxAgent("Minimax", 3, eval_fn = offensive_eval_1)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn = offensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, display=True, progress=True)
    print(res)
    w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=offensive_eval_2)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display=True)
    print(res)
    w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_2)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=offensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display=True)
    print(res)
    w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=offensive_eval_2)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=offensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display = True)
    print(res)
    w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_2)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display = True)
    print(res)
    w_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=offensive_eval_2)
    b_agent = AlphaBetaAgent("Alphabeta", 3, eval_fn=defensive_eval_2)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display = True)
    print(res)



    ...  # YOUR EXPERIMENTS HERE


if __name__ == '__main__':
    main()
