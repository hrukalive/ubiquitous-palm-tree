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
# YOUR NAME: Kyle Chang
# YOUR WPI ID: 90102487
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

def print_board(state):
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    print("\nFinal Board State:")
    for r in range(8):
        print("".join(chars[state["board"][r][c]] for c in range(8)))


def run_matchup(white_agent, black_agent, games=1):
    print("=" * 70)
    print(f"Matchup: {white_agent.name} (White) vs {black_agent.name} (Black)")
    print("=" * 70)

    for i in range(games):
        print(f"\n--- Game {i+1} ---")

        game = Breakthrough()
        state = game.initial_state()

        # Play the game
        results = play_game(
            white_agent,
            black_agent,
            max_moves=400,
            display=False,
            progress=False,
        )

        # Reconstruct final state for board printing
        state = game.initial_state()
        move_count = 0
        while True:
            move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game, state)
            state = game.result(state, move)
            move_count += 1
            if game.terminal_test(state) or move_count >= 400:
                break

        # A. Final Board and Winner
        print_board(state)
        print("\nWinner:", results["winner"])
        print("Total Moves:", results["total_moves"])

        # B. Total nodes expanded
        print("\nTotal Nodes Expanded:")
        print("White:", results["white_nodes"])
        print("Black:", results["black_nodes"])

        # C. Average nodes + time
        print("\nAverage Nodes per Move:")
        print("White:", round(results["white_nodes_per_move"], 2))
        print("Black:", round(results["black_nodes_per_move"], 2))

        print("\nAverage Time per Move (seconds):")
        print("White:", round(results["white_time_per_move"], 5))
        print("Black:", round(results["black_time_per_move"], 5))

        # D. Captures
        print("\nCaptures:")
        print("White captured:", results["white_captures"])
        print("Black captured:", results["black_captures"])

        print("\n")


def main():
    minimax_depth = 3
    alphabeta_depth = 4

    # 1) Minimax (Off1) vs Alpha-beta (Off1)
    run_matchup(
        MinimaxAgent("Minimax Off1", minimax_depth, offensive_eval_1),
        AlphaBetaAgent("AlphaBeta Off1", alphabeta_depth, offensive_eval_1),
    )

    # 2) Alpha-beta (Off2) vs Alpha-beta (Def1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", alphabeta_depth, offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", alphabeta_depth, defensive_eval_1),
    )

    # 3) Alpha-beta (Def2) vs Alpha-beta (Off1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", alphabeta_depth, defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", alphabeta_depth, offensive_eval_1),
    )

    # 4) Alpha-beta (Off2) vs Alpha-beta (Off1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", alphabeta_depth, offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", alphabeta_depth, offensive_eval_1),
    )

    # 5) Alpha-beta (Def2) vs Alpha-beta (Def1)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Def2", alphabeta_depth, defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", alphabeta_depth, defensive_eval_1),
    )

    # 6) Alpha-beta (Off2) vs Alpha-beta (Def2)
    run_matchup(
        AlphaBetaAgent("AlphaBeta Off2", alphabeta_depth, offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def2", alphabeta_depth, defensive_eval_2),
    )


if __name__ == "__main__":
    main()
