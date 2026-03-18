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
# YOUR NAME: Prince Nanakobi Jr
# ID: 901015284
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
# Perform the necessary experiments here to generate data required by the report.
def _board_as_strings(state):
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    return ["".join(chars[state["board"][r][c]] for c in range(8)) for r in range(8)]


def play_game_with_final_state(white_agent, black_agent, max_moves=400):
    """Like breakthrough.play_game, but also returns the final board/state."""
    game = Breakthrough()
    state = game.initial_state()

    move_count = 0
    while True:
        if state["to_move"] == "WHITE":
            move = white_agent.select_move(game, state)
        else:
            move = black_agent.select_move(game, state)

        state = game.result(state, move)
        move_count += 1

        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves and game.terminal_test(state):
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break

    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = (sum(white_agent.time_per_move) / max(1, len(white_agent.time_per_move)))
    black_time_per_move = (sum(black_agent.time_per_move) / max(1, len(black_agent.time_per_move)))
    white_nodes_per_move = white_nodes / max(1, len(white_agent.nodes_per_move))
    black_nodes_per_move = black_nodes / max(1, len(black_agent.nodes_per_move))

    return {
        "winner": "white" if winner == "WHITE" else "black" if winner == "BLACK" else None,
        "white_name": white_agent.name,
        "black_name": black_agent.name,
        "total_moves": move_count,
        "white_nodes": white_nodes,
        "black_nodes": black_nodes,
        "white_nodes_per_move": white_nodes_per_move,
        "black_nodes_per_move": black_nodes_per_move,
        "white_time_per_move": white_time_per_move,
        "black_time_per_move": black_time_per_move,
        "white_captures": state["captures"]["WHITE"],
        "black_captures": state["captures"]["BLACK"],
        "final_board": _board_as_strings(state),
    }


def main():
    # Depths: minimax 3 (feasible), alpha-beta deeper.
    minimax_depth = 3
    alphabeta_depth = 4

    matchups = [
        ("1) Minimax(Off1) vs AlphaBeta(Off1)",
         MinimaxAgent("Minimax Off1", depth=minimax_depth, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)),
        ("2) AlphaBeta(Off2) vs AlphaBeta(Def1)",
         AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1)),
        ("3) AlphaBeta(Def2) vs AlphaBeta(Off1)",
         AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)),
        ("4) AlphaBeta(Off2) vs AlphaBeta(Off1)",
         AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)),
        ("5) AlphaBeta(Def2) vs AlphaBeta(Def1)",
         AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1)),
        ("6) AlphaBeta(Off2) vs AlphaBeta(Def2)",
         AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2)),
    ]

    results = {}
    for title, w_agent, b_agent in matchups:
        # Reset per-run stats in case this script is extended later.
        w_agent.reset()
        b_agent.reset()

        res = play_game_with_final_state(w_agent, b_agent, max_moves=400)
        results[title] = res
        print(title)
        print(json.dumps(res, indent=2))
        print("-" * 60)

    # Save a machine-readable copy for your report.
    with open("experiment_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Wrote experiment_results.json")


if __name__ == "__main__":
    main()
