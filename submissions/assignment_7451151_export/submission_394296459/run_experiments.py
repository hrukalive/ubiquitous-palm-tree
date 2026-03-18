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
# YOUR NAME: Patricia Oltra
# YOUR WPI ID: 901020137
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

    MinimaxOff1 = MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1)
    ABOff1 = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    ABOff2 = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    ABDef1 = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    ABDef2 = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)

    results1 = play_game(MinimaxOff1, ABOff1, max_moves=400, display=False, progress=True)
    print(results1)

    results2 = play_game(ABOff2, ABDef1, max_moves=400, display=False, progress=True)
    print(results2)

    results3 = play_game(ABDef2, ABOff1, max_moves=400, display=False, progress=True)
    print(results3)

    results4 = play_game(ABOff2, ABOff1, max_moves=400, display=False, progress=True)
    print(results4)

    results5 = play_game(ABDef2, ABDef1, max_moves=400, display=False, progress=True)
    print(results5)

    results6 = play_game(ABOff2, ABDef2, max_moves=400, display=False, progress=True)
    print(results6)

    # YOUR EXPERIMENTS HERE


if __name__ == '__main__':
    main()
