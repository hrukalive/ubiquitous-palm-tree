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
# YOUR NAME: Damon Chase
# YOUR WPI ID: 901012024
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
    # Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
    w_agent = MinimaxAgent("Minimax", 2, eval_fn=offensive_eval_1)
    b_agent = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_1)
    res = play_game(w_agent, b_agent, max_moves=400, progress=True, display=True)
    print("Game 1:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])

    
    # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    w_agent2 = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_2)
    b_agent2 = AlphaBetaAgent("Alphabeta", 2, eval_fn=defensive_eval_1)
    res = play_game(w_agent2, b_agent2, max_moves=400, progress=True, display=True)
    print("Game 2:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])


    # Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    w_agent3 = AlphaBetaAgent("Alphabeta", 2, eval_fn=defensive_eval_2)
    b_agent3 = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_1)
    res = play_game(w_agent3, b_agent3, max_moves=400, progress=True, display=True)
    print("Game 3:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])


    # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    w_agent4 = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_2)
    b_agent4 = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_1) 
    res = play_game(w_agent4, b_agent4, max_moves=400, progress=True, display=True)
    print("Game 4:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])


    # Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    w_agent5 = AlphaBetaAgent("Alphabeta", 2, eval_fn=defensive_eval_2)
    b_agent5 = AlphaBetaAgent("Alphabeta", 2, eval_fn=defensive_eval_1)
    res = play_game(w_agent5, b_agent5, max_moves=400, progress=True, display=True)
    print("Game 5:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])


    # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
    w_agent6 = AlphaBetaAgent("Alphabeta", 2, eval_fn=offensive_eval_2) 
    b_agent6 = AlphaBetaAgent("Alphabeta", 2, eval_fn=defensive_eval_2)
    res = play_game(w_agent6, b_agent6, max_moves=400, progress=True, display=True)
    print("Game 6:")
    print(f"Winner: {res['winner']}, {res['white_name'] if res['winner'] == 'white' else res['black_name']}")

    # The total number of game tree nodes expanded by each player in the course of the game.
    print("Total white expanded nodes:", res['white_nodes'])
    print("Total black expanded nodes:", res['black_nodes'])

    # The average number of nodes expanded per move and the average amount of time to make a move.
    print("Average nodes expanded per move for White:", res['white_nodes_per_move'])
    print("Average nodes expanded per move for Black:", res['black_nodes_per_move'])
    print("Average time per move for White:", res['white_time_per_move'])
    print("Average time per move for Black:", res['black_time_per_move'])

    # The number of opponent workers captured by each player, as well as the total number of moves required till the win.
    print("White captures:", res['white_captures'])
    print("Black captures:", res['black_captures'])
    print("Total moves of game:", res['total_moves'])

if __name__ == '__main__':
    main()
