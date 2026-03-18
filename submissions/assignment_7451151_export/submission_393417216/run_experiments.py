import json

from breakthrough import offensive_eval_1, defensive_eval_1, Breakthrough
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME

# YOUR NAME: Shawn Patel
# YOUR WPI ID: 901002838
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm



# Perform the necessary experiments here to generate data required by the report.


def print_result(matchup_num, description, result, final_board):
    """Pretty-print a single matchup result."""
    print(f"\n{'='*60}")
    print(f"Matchup {matchup_num}: {description}")
    print(f"{'='*60}")
    winner_str = result["winner"].upper() if result["winner"] else "DRAW (max moves)"
    print(f"Winner: {winner_str}")
    print(f"Total moves: {result['total_moves']}")

    ####HERE

    print(f"\nWhite ({result['white_name']}):")
    print(f"  Total nodes expanded  : {result['white_nodes']}")
    print(f"  Avg nodes/move        : {result['white_nodes_per_move']:.1f}")
    print(f"  Avg time/move (s)     : {result['white_time_per_move']:.4f}")
    print(f"  Pieces captured       : {result['white_captures']}")

    print(f"\nBlack ({result['black_name']}):")
    print(f"  Total nodes expanded  : {result['black_nodes']}")
    print(f"  Avg nodes/move        : {result['black_nodes_per_move']:.1f}")
    print(f"  Avg time/move (s)     : {result['black_time_per_move']:.4f}")
    print(f"  Pieces captured       : {result['black_captures']}")

def main():
    matchups = [
        # (white_agent, black_agent, description)
        (
            MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
            "Minimax (Off1) vs Alpha-beta (Off1)",
        ),
        (
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
            "Alpha-beta (Off2) vs Alpha-beta (Def1)",
        ),
        (
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
            "Alpha-beta (Def2) vs Alpha-beta (Off1)",
        ),
        (
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
            "Alpha-beta (Off2) vs Alpha-beta (Off1)",
        ),
        (
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
            "Alpha-beta (Def2) vs Alpha-beta (Def1)",
        ),
        (
            AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            "Alpha-beta (Off2) vs Alpha-beta (Def2)",
        ),
    ]

    all_results = []
    for i, (white_agent, black_agent, description) in enumerate(matchups, start=1):
        print(f"\nRunning matchup {i}: {description} ...")
        result = play_game(white_agent, black_agent, max_moves=400, display=True, progress=False)

        print(result)
        all_results.append({
            "matchup": i,
            "description": description,
            # "final_board": result['final_board'],
            **result,
        })

    # Save results to JSON for report use
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\n\nAll results saved to experiment_results.json")


if __name__ == '__main__':
    main()
