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
# YOUR NAME: Wen Hao Chen
# YOUR WPI ID: 997075315
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

DEPTH = 3
MAX_MOVES = 400

def run_matchup(white_agent, black_agent):
    print(f"\n{white_agent.name} (White) vs {black_agent.name} (Black)")
    results = play_game(
        white_agent,
        black_agent,
        max_moves=MAX_MOVES,
        display=False,
        progress=True
    )
    print(results)
    return results

def main():
    # 1) Minimax (Off1) vs Alpha-beta (Off1)
    run_matchup(
        MinimaxAgent("Minimax Off1", depth=DEPTH, eval_fn=offensive_eval_1),
        AlphaBetaAgent("AlphaBeta Off1", depth=DEPTH, eval_fn=offensive_eval_1)
    )

    # 2) Alpha-beta (Off2) vs Alpha-beta (Def1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=DEPTH, eval_fn=defensive_eval_1)
    )

    # 3) Alpha-beta (Def2) vs Alpha-beta (Off1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=DEPTH, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=DEPTH, eval_fn=offensive_eval_1)
    )

    # 4) Alpha-beta (Off2) vs Alpha-beta (Off1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=DEPTH, eval_fn=offensive_eval_1)
    )

    # 5) Alpha-beta (Def2) vs Alpha-beta (Def1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=DEPTH, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=DEPTH, eval_fn=defensive_eval_1)
    )

    # 6) Alpha-beta (Off2) vs Alpha-beta (Def2)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def2", depth=DEPTH, eval_fn=defensive_eval_2)
    )


if __name__ == '__main__':
    main()
