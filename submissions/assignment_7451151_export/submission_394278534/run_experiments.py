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
# YOUR NAME: Chloe Polit
# YOUR WPI ID: 901014956
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

# Perform the necessary experiments here to generate data required by the report.

def main():
    matchups = [
        # matchup number, white pieces, black pieces
        (1, MinimaxAgent("Minimax Offensive Evaluation 1", depth=3, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Offensive Evaluation 1", depth=4, eval_fn=offensive_eval_1)),
        (2, AlphaBetaAgent("AlphaBeta Offensive Evaluation 2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Defensive Evaluation 1", depth=4, eval_fn=defensive_eval_1)),
        (3, AlphaBetaAgent("AlphaBeta Defensive Evaluation 2", depth=4, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Offensive Evaluation 1", depth=4, eval_fn=offensive_eval_1)),
        (4, AlphaBetaAgent("AlphaBeta Offensive Evaluation 2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Offensive Evaluation 1", depth=4, eval_fn=offensive_eval_1)),
        (5, AlphaBetaAgent("AlphaBeta Defensive Evaluation 2", depth=4, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Defensive Evaluation 1", depth=4, eval_fn=defensive_eval_1)),
        (6, AlphaBetaAgent("AlphaBeta Offensive Evaluation 2", depth=4, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Defensive Evaluation 2", depth=4, eval_fn=defensive_eval_2)),
    ]

    for matchup_num, white_agent, black_agent in matchups:
        print(f"MATCHUP {matchup_num}: {white_agent.name} (WHITE) vs {black_agent.name} (BLACK)")

        results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)

        # print results
        print(f"\nA. Winner: {results['winner'].upper() if results['winner'] else 'DRAW'}")

        print(f"\nB. Total nodes expanded:")
        print(f"    WHITE ({results['white_name']}): {results['white_nodes']:,}")
        print(f"    BLACK ({results['black_name']}): {results['black_nodes']:,}")

        print(f"\nC. Average nodes per move:")
        print(f"    WHITE ({results['white_name']}): {results['white_nodes_per_move']:,.3f} nodes/move")
        print(f"    BLACK ({results['black_name']}): {results['black_nodes_per_move']:,.3f} nodes/move")
        print(f"    Average time per move:")
        print(f"    WHITE ({results['white_name']}): {results['white_time_per_move']:.3f} sec/move")
        print(f"    BLACK ({results['black_name']}): {results['black_time_per_move']:.3f} sec/move")

        print(f"\nD. Opponent captures & number of moves:")
        print(f"    WHITE captured: {results['white_captures']} BLACK pieces")
        print(f"    BLACK captured: {results['black_captures']} WHITE pieces")
        print(f"    Total moves: {results['total_moves']}")


if __name__ == '__main__':
    main()
