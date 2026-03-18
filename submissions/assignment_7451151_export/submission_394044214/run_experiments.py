import json

from breakthrough import offensive_eval_1, offensive_eval_2, defensive_eval_2
from breakthrough import defensive_eval_1
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
# YOUR NAME: Benjamin Weber
# YOUR WPI ID: 901008220
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
    minimaxOff1 = MinimaxAgent("Minimax off1", depth=3, eval_fn=offensive_eval_1)

    alphaBetaOff1 = AlphaBetaAgent("AlphaBeta off1", depth=4, eval_fn=offensive_eval_1)
    alphaBetaDef1 = AlphaBetaAgent("AlphaBeta def1", depth=4, eval_fn=defensive_eval_1)
    alphaBetaOff2 = AlphaBetaAgent("AlphaBeta off2", depth=4, eval_fn=offensive_eval_2)
    alphaBetaDef2 = AlphaBetaAgent("AlphaBeta def2", depth=4, eval_fn=defensive_eval_2)

    results = [None] * 6
    results[0] = play_game(minimaxOff1, alphaBetaOff1, max_moves=400, display=True)
    results[1] = play_game(alphaBetaOff2, alphaBetaDef1, max_moves=400, display=True)
    results[2] = play_game(alphaBetaDef2, alphaBetaOff1, max_moves=400, display=True)
    results[3] = play_game(alphaBetaOff2, alphaBetaOff1, max_moves=400, display=True)
    results[4] = play_game(alphaBetaDef2, alphaBetaDef1, max_moves=400, display=True)
    results[5] = play_game(alphaBetaOff2, alphaBetaDef2, max_moves=400, display=True)

    for res in results:
        print('\n\nReport: ' + res['white_name'] + ' vs. ' + res['black_name'] + '\nWinner: ' + res['winner'])
        print('Black Nodes Expanded: ' + str(res['black_nodes']) + 'nodes | White Nodes Expanded: ' + str(res['white_nodes']) + ' nodes')
        print('Average Black Nodes per Move: ' + str(res['black_nodes_per_move']) + 'nodes | Average White Nodes per Move: ' + str(res['white_nodes_per_move']) + 'nodes')
        print('Average Black Time per Move' + str(res['black_time_per_move']) + ' Average White Time per Move: ' + str(res['white_time_per_move']))
        print('Black Captures: ' + str(res['black_captures']) + ' | White Captures: ' + str(res['white_captures']))
        print('Total Moves: ' + str(res['total_moves']) + '\n\n\n')



if __name__ == '__main__':
    main()
