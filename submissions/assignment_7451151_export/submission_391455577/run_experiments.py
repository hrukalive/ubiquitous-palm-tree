import json

from numpy.ma.extras import average

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
from src.breakthrough_agent import minimax_cutoff_search


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Cameron Pietraski
# YOUR WPI ID: 356710957
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
# Perform the necessary experiments here to generate data required by the report.

def main():
    player1 = AlphaBetaAgent("Alphabeta Offensive 2", 5, offensive_eval_2)
    player2 = AlphaBetaAgent("Alphabeta Defensive 2", 5, defensive_eval_2)
    play_game(player1, player2,  display=True, progress=False)

    print(player1.name)
    print("Average nodes: ", average(player1.nodes_per_move))
    print("Average time: ", average(player1.time_per_move))
    print(player2.name)
    print("Average nodes: ", average(player2.nodes_per_move))
    print("Average time: ", average(player2.time_per_move))


if __name__ == '__main__':
    main()
