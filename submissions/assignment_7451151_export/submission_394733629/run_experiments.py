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
# YOUR NAME: Brayden Little
# YOUR WPI ID: 901026978
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

    # matchup 1: minimax o_e_1 vs alphabeta o_e_1
    print("minimax o_e_1 vs alphabeta o_e_1")
    white_agent = MinimaxAgent("minimax o_e_1", 4, offensive_eval_1)
    black_agent = AlphaBetaAgent("alphabeta o_e_1", 4, offensive_eval_1)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)

    # matchup 2: alphabeta o_e_2 vs alphabeta d_e_1
    print("alphabeta o_e_2 vs alphabeta d_e_1")
    white_agent = AlphaBetaAgent("alphabeta o_e_2", 4, offensive_eval_2)
    black_agent = AlphaBetaAgent("alphabeta d_e_1", 4, defensive_eval_1)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)

    # matchup 3: alphabeta d_e_2 vs alphabeta o_e_1
    print("alphabeta d_e_2 vs alphabeta o_e_1")
    white_agent = AlphaBetaAgent("alphabeta d_e_2", 4, defensive_eval_2)
    black_agent = AlphaBetaAgent("alphabeta o_e_1", 4, offensive_eval_1)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)

    # matchup 4: alphabeta o_e_2 vs alphabeta o_e_1
    print("alphabeta o_e_2 vs alphabeta o_e_1")
    white_agent = AlphaBetaAgent("alphabeta o_e_2", 4, offensive_eval_2)
    black_agent = AlphaBetaAgent("alphabeta o_e_1", 4, offensive_eval_1)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)

    # matchup 5: alphabeta d_e_2 vs alphabeta d_e_1
    print("alphabeta d_e_2 vs alphabeta d_e_1")
    white_agent = AlphaBetaAgent("alphabeta d_e_2", 4, defensive_eval_2)
    black_agent = AlphaBetaAgent("alphabeta d_e_1", 4, defensive_eval_1)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)

    # matchup 6: alphabeta o_e_2 vs alphabeta d_e_2
    print("alphabeta o_e_2 vs alphabeta d_e_2")
    white_agent = AlphaBetaAgent("alphabeta o_e_2", 4, offensive_eval_2)
    black_agent = AlphaBetaAgent("alphabeta d_e_2", 4, defensive_eval_2)
    game_results = play_game(white_agent, black_agent, max_moves=400)
    print_results(game_results)


def print_results(game_results):
    # Print experiment stats
    print("Winner = ", game_results["winner"])
    from breakthrough import Breakthrough
    game = Breakthrough()
    print("Final board state = ")
    game.display(game_results["final_board"])
    print("White total nodes =  ", game_results["white_nodes"])
    print("Black total nodes =  ", game_results["black_nodes"])
    print("White average nodes per move = ", game_results["white_nodes_per_move"])
    print("Black average nodes per move = ", game_results["black_nodes_per_move"])
    print("White average time per move = ", game_results["white_time_per_move"])
    print("Black average time per move = ", game_results["black_time_per_move"])
    print("White captures = ", game_results["white_captures"])
    print("Black captures = ", game_results["black_captures"])
    print("Total moves =  ", game_results["total_moves"])

if __name__ == '__main__':
    main()