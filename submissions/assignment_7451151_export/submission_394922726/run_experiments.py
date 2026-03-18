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
# YOUR NAME: Vincent Grassi
# YOUR WPI ID: 901018161
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
def experiment(label, white_agent, black_agent, max_moves=100):
    from breakthrough import Breakthrough

    # Saves starting board by intercepted state when result is called
    original_board = Breakthrough.result
    final_board = {"state": None}

    # Temporary wrapper around result to save the board
    def capture_board(self, s, a):
        ns = original_board(self, s, a)
        final_board["state"] = ns
        return ns
    Breakthrough.result = capture_board

    try:
        res = play_game(white_agent, black_agent, max_moves=max_moves, display=False, progress=True)
    finally:
        # Resets board
        Breakthrough.result = original_board

    # Prints summary game statistics
    print(label)
    print(f"Total moves: {res['total_moves']}")
    print(f"Total nodes: White {res['white_nodes']} | Black {res['black_nodes']}")
    print(f"Avg nodes per move: White {res['white_nodes_per_move']:.2f} | Black {res['black_nodes_per_move']:.2f}")
    print(f"Avg time per move:  White {res['white_time_per_move']:.4f}s | Black {res['black_time_per_move']:.4f}s")

    # Prints final board position
    if final_board["state"] is not None:
        print("\nFinal Board:")
        game = Breakthrough()
        game.display(final_board["state"])
    else:
        print("\nFinal Board: (could not capture)")

    print("\n" + "-" * 50)


def main():
    MM_DEPTH = 3
    AB_DEPTH = 4

    experiment("1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)",
        MinimaxAgent("MM Off1", depth=MM_DEPTH, eval_fn=offensive_eval_1),
        AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1))

    experiment("2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)",
        AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AB Def1", depth=AB_DEPTH, eval_fn=defensive_eval_1))

    experiment("3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)",
        AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1))

    experiment("4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)",
        AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1))

    experiment("5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)",
        AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AB Def1", depth=AB_DEPTH, eval_fn=defensive_eval_1))

    experiment("6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)",
        AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2))



    # experiment("1) Alpha-beta (Offensive Evaluation 1) vs Minimax (Offensive Evaluation 1)",
    #            AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1),
    #            MinimaxAgent("MM Off1", depth=MM_DEPTH, eval_fn=offensive_eval_1))
    #
    # experiment("2) Alpha-beta (Defensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 2)",
    #            AlphaBetaAgent("AB Def1", depth=AB_DEPTH, eval_fn=defensive_eval_1),
    #            AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2))
    #
    # experiment("3) Alpha-beta (Offensive Evaluation 1) vs Alpha-beta (Defensive Evaluation 2)",
    #            AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1),
    #            AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2))
    #
    # experiment("4) Alpha-beta (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 2)",
    #            AlphaBetaAgent("AB Off1", depth=AB_DEPTH, eval_fn=offensive_eval_1),
    #            AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2))
    #
    # experiment("5) Alpha-beta (Defensive Evaluation 1) vs Alpha-beta (Defensive Evaluation 2)",
    #            AlphaBetaAgent("AB Def1", depth=AB_DEPTH, eval_fn=defensive_eval_1),
    #            AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2))
    #
    # experiment("6) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 2)",
    #            AlphaBetaAgent("AB Def2", depth=AB_DEPTH, eval_fn=defensive_eval_2),
    #            AlphaBetaAgent("AB Off2", depth=AB_DEPTH, eval_fn=offensive_eval_2))


if __name__ == "__main__":
    main()
