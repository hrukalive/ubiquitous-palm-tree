import json

from concurrent.futures import ProcessPoolExecutor, as_completed
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
# YOUR NAME: Hunter Boles
# YOUR WPI ID: 646321181
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

def single_game(white_is_agent_1, agent_1_config, agent_2_config, progress = False):
    agent_1 = agent_1_config["agent"](agent_1_config["name"], eval_fn=agent_1_config["eval_fn"])
    agent_2 = agent_2_config["agent"](agent_2_config["name"], eval_fn=agent_2_config["eval_fn"])
    
    if white_is_agent_1:
        res = play_game(agent_1, agent_2, max_moves=400, progress=progress)
        winner = res["winner"] == "white"
        return winner, res
    else:
        res = play_game(agent_2, agent_1, max_moves=400, progress=progress)
        winner = res["winner"] == "black"
        return winner, res


def test(test_amount, agent_1_config, agent_2_config, max_workers=None):
    win_count_agent_1 = 0
    win_count_agent_2 = 0

    tasks = [True] * test_amount + [False] * test_amount
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_game, t, agent_1_config, agent_2_config) for t in tasks]
        for future in as_completed(futures):
            winner, res = future.result()
            if winner:
                win_count_agent_1 += 1
            else:
                win_count_agent_2 += 1
            results.append(res)

    return win_count_agent_1, win_count_agent_2, results

def main():
    # YOUR EXPERIMENTS HERE
    
    games = [
        (
            dict(agent=MinimaxAgent,   name="minimax_off1",   eval_fn=offensive_eval_1),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off1",   eval_fn=offensive_eval_1)
        ),
        (
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off2",   eval_fn=offensive_eval_2),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_def1",   eval_fn=defensive_eval_1)
        ),
        (
            dict(agent=AlphaBetaAgent,   name="alpha_beta_def2",   eval_fn=defensive_eval_2),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off1",   eval_fn=offensive_eval_1)
        ),
        (
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off2",   eval_fn=offensive_eval_2),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off1",   eval_fn=offensive_eval_1)
        ),
        (
            dict(agent=AlphaBetaAgent,   name="alpha_beta_def2",   eval_fn=defensive_eval_2),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_def1",   eval_fn=defensive_eval_1)
        ),
        (
            dict(agent=AlphaBetaAgent,   name="alpha_beta_off2",   eval_fn=offensive_eval_2),
            dict(agent=AlphaBetaAgent,   name="alpha_beta_def2",   eval_fn=defensive_eval_2)
        )
    ]

    for game in games:
        print("----------------------------------")
        print("Game: {} vs {}".format(game[0]['name'], game[1]['name']))
        win_count_agent_1, win_count_agent_2, results = test(1, game[0], game[1])
        for i in range(len(results)):
            res = results[i]
            print("-----------------------------")
            print("result {}".format(i))
            avg_node = res['white_nodes_per_move'] + res['black_nodes_per_move'] / 2
            avg_time = res['white_time_per_move'] + res['black_time_per_move'] / 2

            print("Total moves: {}".format(res['total_moves']))
            print("Winner: {}".format(res['winner']))
            print("--------")
            print("White")
            print("Name: {}".format(res['white_name']))
            print("Total nodes: {}".format(res['white_nodes']))
            print("Total captures: {}".format(res['white_captures']))
            print("Nodes per move: {}".format(res['white_nodes_per_move']))
            print("Time per move: {}".format(res['white_time_per_move']))

            print("--------")
            print("Black")
            print("Name: {}".format(res['black_name']))
            print("Total nodes: {}".format(res['black_nodes']))
            print("Total captures: {}".format(res['black_captures']))
            print("Nodes per move: {}".format(res['black_nodes_per_move']))
            print("Time per move: {}".format(res['black_time_per_move']))

            print("--------")
            print("Final Board")
            board = res['state']['board']
            for row in range(len(board)):
                for col in range(len(board[0])):
                    cell = board[row][col]
                    if cell == "WHITE": 
                        print("W", end=" ")
                    elif cell == "BLACK":
                        print("B", end=" ")
                    else:
                        print(".", end=" ")
                print()
            
            print("--------")
            print("Average nodes expanded per move: {}".format(avg_node))
            print("Average time expanded per move: {}".format(avg_time))


        print("-----------------------------")
        print("{}:{}, {}:{}".format(game[0]['name'], win_count_agent_1, game[1]['name'], win_count_agent_2))



if __name__ == '__main__':
    main()
