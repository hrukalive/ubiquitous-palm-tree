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
# YOUR NAME: Max Williams
# YOUR WPI ID: 162250303
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

NUM_GAMES = 3
MINIMAX_DEPTH = 3
ALPHABETA_DEPTH = 4
MAX_MOVES = 400

def run_matchup(white_agent, black_agent, matchup_name):
    print("="*70)
    print(f"Matchup: {matchup_name}")
    print("="*70)

    results = play_game(white_agent, black_agent, max_moves=MAX_MOVES, progress=True, display=False)

    # --------------------------
    # A. Final board
    # --------------------------
    print("\nFinal board:")
    game = Breakthrough()
    final_state = {
        'board': results['final_board'],
        'to_move': results['to_move'],
        'captures': {
            'WHITE': results['white_captures'],
            'BLACK': results['black_captures']
        }
    }
    game.display(final_state)
    print(f"Winner: {results['winner']}\n")

    # --------------------------
    # B. Total nodes expanded
    # --------------------------
    print(f"Total nodes expanded:")
    print(f"  White ({results['white_name']}): {results['white_nodes']}")
    print(f"  Black ({results['black_name']}): {results['black_nodes']}\n")

    # --------------------------
    # C. Average nodes per move and time per move
    # --------------------------
    print(f"Average per move:")
    print(f"  White: {results['white_nodes_per_move']:.1f} nodes, {results['white_time_per_move']:.3f}s")
    print(f"  Black: {results['black_nodes_per_move']:.1f} nodes, {results['black_time_per_move']:.3f}s\n")

    # --------------------------
    # D. Captures and total moves
    # --------------------------
    print(f"Captures and moves:")
    print(f"  White captured: {results['white_captures']}")
    print(f"  Black captured: {results['black_captures']}")
    print(f"  Total moves: {results['total_moves']}")
    print("\n\n")


def main():
    # ==========================
    # Matchup 1: Minimax (Offensive Eval 1) vs AlphaBeta (Offensive Eval 1)
    # ==========================
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        MinimaxAgent("MiniMax Off1", depth=3, eval_fn=offensive_eval_1),
        "AlphaBeta (Off1) vs MiniMax (Off1)"
    )

    # Matchup 2: AlphaBeta (Offensive Eval 2) vs AlphaBeta (Defensive Eval 1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1),
        "AlphaBeta (Off2) vs AlphaBeta (Def1)"
    )

    # Matchup 3: AlphaBeta (Defensive Eval 2) vs AlphaBeta (Offensive Eval 1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1),
        "AlphaBeta (Def2) vs AlphaBeta (Off1)"
    )

    # Matchup 4: AlphaBeta (Offensive Eval 2) vs AlphaBeta (Offensive Eval 1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1),
        "AlphaBeta (Off2) vs AlphaBeta (Off1)"
    )

    # Matchup 5: AlphaBeta (Defensive Eval 2) vs AlphaBeta (Defensive Eval 1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1),
        "AlphaBeta (Def2) vs AlphaBeta (Def1)"
    )

    # Matchup 6: AlphaBeta (Offensive Eval 2) vs AlphaBeta (Defensive Eval 2)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2),
        "AlphaBeta (Off2) vs AlphaBeta (Def2)"
    )


if __name__ == "__main__":
    main()
