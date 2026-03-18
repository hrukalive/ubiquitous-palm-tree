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
# YOUR NAME: Connor Daniel
# YOUR WPI ID: 901010829
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
    # 1) Minimax (Off1) vs AlphaBeta (Off1)
    agent1 = MinimaxAgent("Minimax Off1", eval_fn=offensive_eval_1)
    agent2 = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    results = play_game(agent1, agent2, display=False)
    print_results("Minimax Off1 vs AlphaBeta Off1", results)

    # 2) AlphaBeta (Off2) vs AlphaBeta (Def1)
    agent1 = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    agent2 = AlphaBetaAgent("AlphaBeta Def1", eval_fn=defensive_eval_1)
    results = play_game(agent1, agent2)
    print_results("AlphaBeta Off2 vs AlphaBeta Def1", results)

    # 3) AlphaBeta (Def2) vs AlphaBeta (Off1)
    agent1 = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    agent2 = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    results = play_game(agent1, agent2)
    print_results("AlphaBeta Def2 vs AlphaBeta Off1", results)

    # 4) AlphaBeta (Off2) vs AlphaBeta (Off1)
    agent1 = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    agent2 = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    results = play_game(agent1, agent2)
    print_results("AlphaBeta Off2 vs AlphaBeta Off1", results)

    # 5) AlphaBeta (Def2) vs AlphaBeta (Def1)
    agent1 = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    agent2 = AlphaBetaAgent("AlphaBeta Def1", eval_fn=defensive_eval_1)
    results = play_game(agent1, agent2)
    print_results("AlphaBeta Def2 vs AlphaBeta Def1", results)

    # 6) AlphaBeta (Off2) vs AlphaBeta (Def2)
    agent1 = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    agent2 = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    results = play_game(agent1, agent2)
    print_results("AlphaBeta Off2 vs AlphaBeta Def2", results)


def print_results(label, results):
    print("\n==============================")
    print("Matchup:", label)
    print("==============================")
    print("Winner:", results['winner'])
    print("Total moves:", results['total_moves'])

    print("\n--- Nodes Expanded ---")
    print("White total nodes:", results['white_nodes'])
    print("Black total nodes:", results['black_nodes'])

    print("\n--- Avg Nodes Per Move ---")
    print("White:", results['white_nodes_per_move'])
    print("Black:", results['black_nodes_per_move'])

    print("\n--- Avg Time Per Move ---")
    print("White:", results['white_time_per_move'])
    print("Black:", results['black_time_per_move'])

    print("\n--- Captures ---")
    print("White captures:", results['white_captures'])
    print("Black captures:", results['black_captures'])
    print("==============================\n")


if __name__ == '__main__':
    main()
