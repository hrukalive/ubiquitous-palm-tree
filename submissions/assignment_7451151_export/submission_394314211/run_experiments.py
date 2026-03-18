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
# YOUR NAME: Nathaniel Rubin
# YOUR WPI ID: 214674091
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
    results = []
    print("result 1")
    results.append(play_game(
        white_agent=MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
        black_agent=AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        max_moves=400, display=True, progress=True))
    print("result 2")
    results.append(play_game(
        white_agent=AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        black_agent=AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        max_moves=400, display=True, progress=True
    ))
    print("result 3")
    results.append(play_game(
        white_agent=AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=offensive_eval_2),
        black_agent=AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=defensive_eval_1),
        max_moves=400, display=True, progress=True
    ))
    print("result 4")
    results.append(play_game(
        white_agent=AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        black_agent=AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        max_moves=400, display=True, progress=True
    ))
    print("result 5")
    results.append(play_game(
        white_agent=AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        black_agent=AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        max_moves=400, display=True, progress=True
    ))
    print("result 6")
    results.append(play_game(
        white_agent=AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        black_agent=AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_1),
        max_moves=400, display=True, progress=True
    ))

    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)


if __name__ == '__main__':
    main()
