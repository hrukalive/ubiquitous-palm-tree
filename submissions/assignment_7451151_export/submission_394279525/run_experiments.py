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
# YOUR NAME: Daniel Tuladhar
# YOUR WPI ID: 901034450
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################

# Perform the necessary experiments here to generate data required by the report.

def main():
    print("Starting Breakthrough Experiments: \n")

    # All tournament matchups 
    matchups = [
        (
            MinimaxAgent("Minimax (Off1)", depth=3, eval_fn=offensive_eval_1),
            AlphaBetaAgent("Alpha-beta (Off1)", depth=4, eval_fn=offensive_eval_1)
        ),
        (
            AlphaBetaAgent("Alpha-beta (Off2)", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("Alpha-beta (Def1)", depth=4, eval_fn=defensive_eval_1)
        ),
        (
            AlphaBetaAgent("Alpha-beta (Def2)", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("Alpha-beta (Off1)", depth=4, eval_fn=offensive_eval_1)
        ),
        (
            AlphaBetaAgent("Alpha-beta (Off2)", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("Alpha-beta (Off1)", depth=4, eval_fn=offensive_eval_1)
        ),
        (
            AlphaBetaAgent("Alpha-beta (Def2)", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("Alpha-beta (Def1)", depth=4, eval_fn=defensive_eval_1)
        ),
        (
            AlphaBetaAgent("Alpha-beta (Off2)", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("Alpha-beta (Def2)", depth=4, eval_fn=defensive_eval_2)
        )
    ]

    for i, (white_agent, black_agent) in enumerate(matchups, 1):
        print(f"\n--------------------------------------------------------------------")
        print(f"Matchup {i}: {white_agent.name} (White) vs {black_agent.name} (Black)")
        print(f"--------------------------------------------------------------------\n")
        
        # Reset tracking stats before the game
        white_agent.reset()
        black_agent.reset()

        # Play the game 
        results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)

        print("\n--- Match Results (For your Report) ---")
        print(f"Winning Player: {results['winner'].upper() if results['winner'] else 'DRAW'}")
        print(f"Total Moves to Win: {results['total_moves']}")
        
        print(f"\n[White] {results['white_name']}:")
        print(f"  - Opponent Workers Captured: {results['white_captures']}")
        print(f"  - Total Nodes Expanded: {results['white_nodes']}")
        print(f"  - Avg Nodes Expanded/Move: {results['white_nodes_per_move']:.2f}")
        print(f"  - Avg Time/Move: {results['white_time_per_move']:.4f} seconds")

        print(f"\n[Black] {results['black_name']}:")
        print(f"  - Opponent Workers Captured: {results['black_captures']}")
        print(f"  - Total Nodes Expanded: {results['black_nodes']}")
        print(f"  - Avg Nodes Expanded/Move: {results['black_nodes_per_move']:.2f}")
        print(f"  - Avg Time/Move: {results['black_time_per_move']:.4f} seconds\n")


if __name__ == '__main__':
    main()
