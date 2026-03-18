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
# YOUR NAME: Shuying Zhao
# YOUR WPI ID: 901017143
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
# Perform the necessary experiments here to generate data required by the report.

def pretty_print(results):

    print("\n==============================")
    print("GAME RESULTS")
    print("==============================\n")

    print("Winner:", results['winner'])
    print("Total Moves:", results['total_moves'])

    print("\n--- WHITE ({}) ---".format(results['white_name']))
    print("Total Nodes Expanded:", results['white_nodes'])
    print("Avg Nodes per Move:", results['white_nodes_per_move'])
    print("Avg Time per Move:", results['white_time_per_move'])
    print("Captures:", results['white_captures'])

    print("\n--- BLACK ({}) ---".format(results['black_name']))
    print("Total Nodes Expanded:", results['black_nodes'])
    print("Avg Nodes per Move:", results['black_nodes_per_move'])
    print("Avg Time per Move:", results['black_time_per_move'])
    print("Captures:", results['black_captures'])

    print("\n==============================\n")

    

def main():
    results1 = play_game(MinimaxAgent("Minimax Offensive 1", 3, offensive_eval_1), AlphaBetaAgent("Alpha-Beta O1", 3, offensive_eval_1))
    results2 = play_game(AlphaBetaAgent("Alpha-Beta O2", 3, offensive_eval_2), AlphaBetaAgent("Alpha-Beta D1", 3, defensive_eval_1))
    results3 = play_game(AlphaBetaAgent("Alpha-Beta D2", 3, defensive_eval_2), AlphaBetaAgent("Alpha-Beta O1", 3, offensive_eval_1))
    results4 = play_game(AlphaBetaAgent("Alpha-Beta O2", 3, offensive_eval_2), AlphaBetaAgent("Alpha-Beta O1", 3, offensive_eval_1))
    results5 = play_game(AlphaBetaAgent("Alpha-Beta D2", 3, defensive_eval_2), AlphaBetaAgent("Alpha-Beta D1", 3, defensive_eval_1))
    results6 = play_game(AlphaBetaAgent("Alpha-Beta O2", 3, offensive_eval_2), AlphaBetaAgent("Alpha-Beta D2", 3, defensive_eval_2))

    pretty_print(results1)
    pretty_print(results2)
    pretty_print(results3)
    pretty_print(results4)
    pretty_print(results5)
    pretty_print(results6)


if __name__ == '__main__':
    main()
