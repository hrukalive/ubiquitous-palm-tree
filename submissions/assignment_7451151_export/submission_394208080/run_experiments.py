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
# YOUR NAME: Xin Yu Wu
# YOUR WPI ID: 901020339
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

def main():
    # Define matchups: (White Agent, Black Agent, White Eval, Black Eval)
    matchups = [
        ("AlphaBeta Off1", "AlphaBeta Def1", offensive_eval_1, defensive_eval_1),
        ("AlphaBeta Off1", "AlphaBeta Def2", offensive_eval_1, defensive_eval_2),
        ("AlphaBeta Off2", "AlphaBeta Def1", offensive_eval_2, defensive_eval_1),
        ("AlphaBeta Off2", "AlphaBeta Def2", offensive_eval_2, defensive_eval_2),
        ("AlphaBeta Def1", "AlphaBeta Off1", defensive_eval_1, offensive_eval_1),
        ("AlphaBeta Def2", "AlphaBeta Off2", defensive_eval_2, offensive_eval_2),
    ]

    results = []
    for i, (white_name, black_name, white_eval, black_eval) in enumerate(matchups, start=1):
        print(f"\n=== Running Matchup {i}: {white_name} vs {black_name} ===")

        white_agent = AlphaBetaAgent(white_name, depth=3, eval_fn=white_eval)
        black_agent = AlphaBetaAgent(black_name, depth=3, eval_fn=black_eval)


        # Run the game with display=False to avoid clutter; progress=True shows progress bar
        game_result = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)

        # Print results
        print(f"Winner: {game_result['winner']}")
        print(f"Total nodes: White={game_result['white_nodes']}, "
              f"Black={game_result['black_nodes']}")
        print(f"Avg nodes/move: White={game_result['white_nodes_per_move']:.2f}, "
              f"Black={game_result['black_nodes_per_move']:.2f}")
        print(f"Avg time/move: White={game_result['white_time_per_move']:.4f}s, "
              f"Black={game_result['black_time_per_move']:.4f}s")
        print(f"Captures: White={game_result['white_captures']}, "
              f"Black={game_result['black_captures']}")
        print(f"Total moves: {game_result['total_moves']}")

        final_board = game_result["final_state"]["board"]
        print("\nFinal Board State:")
        for row in final_board:
            print(" ".join(row))

        results.append(game_result)



    print("\nAll matchups complete.")








if __name__ == '__main__':
    main()
