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
# YOUR NAME: Theo Sawters
# YOUR WPI ID: 553322480 
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
def run_matchup(white_agent, black_agent, matchup_num):
    print(f"\n{'='*60}")
    print(f"Matchup {matchup_num}: {white_agent.name} (WHITE) vs {black_agent.name} (BLACK)")
    print('='*60)
    
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    
    print(f"\nWinner: {results['winner']}")
    print(f"Total moves: {results['total_moves']}")
    print(f"\nWHITE ({results['white_name']}):")
    print(f"  Total nodes expanded: {results['white_nodes']}")
    print(f"  Avg nodes per move: {results['white_nodes_per_move']:.2f}")
    print(f"  Avg time per move: {results['white_time_per_move']:.4f}s")
    print(f"  Captures: {results['white_captures']}")
    print(f"\nBLACK ({results['black_name']}):")
    print(f"  Total nodes expanded: {results['black_nodes']}")
    print(f"  Avg nodes per move: {results['black_nodes_per_move']:.2f}")
    print(f"  Avg time per move: {results['black_time_per_move']:.4f}s")
    print(f"  Captures: {results['black_captures']}")
    
    return results
def main():
    all_results = {}

    # 1) Minimax (Offensive 1) vs Alpha-beta (Offensive 1)
    all_results['matchup_1'] = run_matchup(
        MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        matchup_num=1
    )

    # 2) Alpha-beta (Offensive 2) vs Alpha-beta (Defensive 1)
    all_results['matchup_2'] = run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        matchup_num=2
    )

    # 3) Alpha-beta (Defensive 2) vs Alpha-beta (Offensive 1)
    all_results['matchup_3'] = run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        matchup_num=3
    )

    # 4) Alpha-beta (Offensive 2) vs Alpha-beta (Offensive 1)
    all_results['matchup_4'] = run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        matchup_num=4
    )

    # 5) Alpha-beta (Defensive 2) vs Alpha-beta (Defensive 1)
    all_results['matchup_5'] = run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        matchup_num=5
    )

    # 6) Alpha-beta (Offensive 2) vs Alpha-beta (Defensive 2)
    all_results['matchup_6'] = run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=defensive_eval_2),
        matchup_num=6
    )

    # Save results to JSON for report
    with open('experiment_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    print("\nResults saved to experiment_results.json")

if __name__ == '__main__':
    main()



