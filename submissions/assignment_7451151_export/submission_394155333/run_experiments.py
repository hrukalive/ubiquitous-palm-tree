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
# YOUR NAME: Raghavan Rajkumar
# YOUR WPI ID: 901014040
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


def board_as_string(board):
    chars = {"WHITE" : "W", "BLACK" : "B", "EMPTY" : "."}
    return ["".join(chars[board[r][c]] for c in range(8)) for r in range(8)]

def play(white, black, max_moves = 400):
    game = Breakthrough()
    state = game.initial_state()
    move_count = 0

    white.reset()
    black.reset()

    while True:
        agent = white if state["to_move"] == "WHITE" else black
        move = agent.select_move(game, state)
        state = game.result(state, move)
        move_count += 1

        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break

    white_nodes = sum(white.nodes_per_move)
    black_nodes = sum(black.nodes_per_move)

    white_nodes_per_move = white_nodes / len(white.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black.nodes_per_move)

    white_time_per_move = sum(white.time_per_move) / len(white.time_per_move)
    black_time_per_move = sum(black.time_per_move) / len(black.time_per_move)

    white_caps = state["captures"]["WHITE"]
    black_caps = state["captures"]["BLACK"]

    print("=" * 80)
    print(f"Matchup {white.name} (White) {black.name} (Black)")
    print("=" * 80)

    rows = board_as_string(state["board"])
    for r in rows:
        print(r)

    print(f"\nWINNER {winner}")

    print("\n Total Nodes Expanded")
    print(f"White: ({white.name}) - {white_nodes}")
    print(f"Black: ({black.name}) - {black_nodes}")

    print("\n Average Nodes Per Move & Average Time Per Move")
    print(f"White: {white_nodes_per_move:.2f} nodes/move, {white_time_per_move:.2f} seconds/move")
    print(f"Black: {black_nodes_per_move:.2f} nodes/move, {black_time_per_move:.2f} seconds/move")

    print("\n Captures & Total Moves")
    print(f"White: {white_caps}, Black: {black_caps}")
    print(f"Total Moves {move_count}")

    print("=" * 80 + "\n")


def main():
    MAX_MOVES = 400

    play(
        MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1), AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1), MAX_MOVES
    )

    play(
        MinimaxAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_1), AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_1), MAX_MOVES
    )

    play(
        MinimaxAgent("AlphaBeta Def2", depth=3, eval_fn=offensive_eval_1), AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1), MAX_MOVES
    )

    play(
        MinimaxAgent("AlphaBeta Def2", depth=3, eval_fn=offensive_eval_1), AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_1), MAX_MOVES
    )

    play(
        MinimaxAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_1), AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=offensive_eval_1), MAX_MOVES
    )


if __name__ == '__main__':
    main()
