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
# YOUR NAME: Daijiro Tanimura
# YOUR WPI ID: 997073434
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
    
    m_depth = 3
    ab_depth = 4

    matchups = [
        (MinimaxAgent("Minimax Off1", depth=m_depth, eval_fn=offensive_eval_1),
         AlphaBetaAgent("Alpha-beta Off1", depth=ab_depth, eval_fn=offensive_eval_1)),

        (AlphaBetaAgent("Alpha-beta Off2", depth=ab_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("Alpha-beta Def1", depth=ab_depth, eval_fn=defensive_eval_1)),

        (AlphaBetaAgent("Alpha-beta Def2", depth=ab_depth, eval_fn=defensive_eval_2),
         AlphaBetaAgent("Alpha-beta Off1", depth=ab_depth, eval_fn=offensive_eval_1)),

        (AlphaBetaAgent("Alpha-beta Off2", depth=ab_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("Alpha-beta Off1", depth=ab_depth, eval_fn=offensive_eval_1)),
        
        (AlphaBetaAgent("Alpha-beta Def2", depth=ab_depth, eval_fn=defensive_eval_2),
         AlphaBetaAgent("Alpha-beta Def1", depth=ab_depth, eval_fn=defensive_eval_1)),
        
        (AlphaBetaAgent("Alpha-beta Off2", depth=ab_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("Alpha-beta Def2", depth=ab_depth, eval_fn=defensive_eval_2)),
    ]


    for i, (white, black) in enumerate(matchups, 1):
        print(f"\n{'='*20} Matchup {i} {'='*20}")
        print(f"White: {white.name} vs Black: {black.name}")

        results = play_game(white, black, max_moves=400, display=True, progress=True)
        
        print(f"\n--- Results for Matchup {i} ---")
        print(f"A. Winner: {results['winner']}")
        print(f"B. Total Nodes Expanded:")
        print(f"   White ({white.name}): {results['white_nodes']}")
        print(f"   Black ({black.name}): {results['black_nodes']}")
        print(f"C. Averages per Move:")
        print(f"   Nodes: White {results['white_nodes_per_move']:.1f}, Black {results['black_nodes_per_move']:.1f}")
        print(f"   Time:  White {results['white_time_per_move']:.4f}s, Black {results['black_time_per_move']:.4f}s")
        print(f"D. Captures & Moves:")
        print(f"   Opponent workers captured by White: {results['white_captures']}")
        print(f"   Opponent workers captured by Black: {results['black_captures']}")
        print(f"   Total moves till win: {results['total_moves']}")

if __name__ == '__main__':
    main()