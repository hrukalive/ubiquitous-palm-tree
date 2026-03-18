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
# YOUR NAME: Zack Savill
# YOUR WPI ID: 901010551
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm



# Perform the necessary experiments here to generate data required by the report.

def main():
    matchups = [
        (MinimaxAgent("MM Off1", 3, offensive_eval_1), AlphaBetaAgent("AB Off1", 3, offensive_eval_1)),
        (AlphaBetaAgent("AB Off2", 3, offensive_eval_2), AlphaBetaAgent("AB Def1", 3, defensive_eval_1)),
        (AlphaBetaAgent("AB Def2", 3, defensive_eval_2), AlphaBetaAgent("AB Off1", 3, offensive_eval_1)),
        (AlphaBetaAgent("AB Off2", 3, offensive_eval_2), AlphaBetaAgent("AB Off1", 3, offensive_eval_1)),
        (AlphaBetaAgent("AB Def2", 3, defensive_eval_2), AlphaBetaAgent("AB Def1", 3, defensive_eval_1)),
        (AlphaBetaAgent("AB Off2", 3, offensive_eval_2), AlphaBetaAgent("AB Def2", 3, defensive_eval_2))
    ]

    for i, (white, black) in enumerate(matchups, 1):
        print(f"\n" + "=" * 50)
        print(f"RUNNING MATCHUP {i}: {white.name} (W) vs {black.name} (B)")
        print("=" * 50)

        res = play_game(white, black, max_moves=400, progress=True)

        print("\n--- Matchup Statistics ---")
        print(f"Winner: {res['winner'].upper() if res['winner'] else 'Draw'}")
        print(f"Total Moves: {res['total_moves']}")

        print(f"\nWhite ({white.name}):")
        print(f"  - Total Nodes Expanded: {res['white_nodes']}")
        print(f"  - Avg Nodes Per Move:   {res['white_nodes_per_move']:.2f}")
        print(f"  - Avg Time Per Move:    {res['white_time_per_move']:.5f}s")
        print(f"  - Opponent Captured:    {res['white_captures']}")

        print(f"\nBlack ({black.name}):")
        print(f"  - Total Nodes Expanded: {res['black_nodes']}")
        print(f"  - Avg Nodes Per Move:   {res['black_nodes_per_move']:.2f}")
        print(f"  - Avg Time Per Move:    {res['black_time_per_move']:.5f}s")
        print(f"  - Opponent Captured:    {res['black_captures']}")

        white.reset()
        black.reset()


if __name__ == '__main__':
    main()
