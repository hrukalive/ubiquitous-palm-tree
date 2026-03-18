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
# YOUR NAME: Amie Binan
# YOUR WPI ID: 901026365
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
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
    with open("results.txt", "w") as f:
        # Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
        print_and_save_results("Minimax Off1", "AlphaBeta Off1", file=f)
        # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        print_and_save_results("AlphaBeta Off2", "AlphaBeta Def1", file=f)
        # Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        print_and_save_results("AlphaBeta Def2", "AlphaBeta Off1", file=f)
        # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        print_and_save_results("AlphaBeta Off2", "AlphaBeta Off1", file=f)
        # Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        print_and_save_results("AlphaBeta Def2", "AlphaBeta Def1", file=f)
        # Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
        print_and_save_results("AlphaBeta Off2", "AlphaBeta Def2", file=f)

def print_and_save_results(white, black, file=None):
    agents = {
        "AlphaBeta Off1": offensive_eval_1,
        "AlphaBeta Off2": offensive_eval_2,
        "AlphaBeta Def1": defensive_eval_1,
        "AlphaBeta Def2": defensive_eval_2,
    }
    if white == "Minimax Off1":
        white_agent = MinimaxAgent("Minimax Off1", depth=3)
    else:
        white_agent = AlphaBetaAgent(white, depth=3, eval_fn=agents[white])
    black_agent = AlphaBetaAgent(black, depth=3, eval_fn=agents[black])

    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    output = list()
    output.append(f"---------- {white} vs {black} ----------")
    output.append(board_to_str(results['final_board']))
    output.append(f"Winner: {results['winner']}")
    output.append(f"White Nodes: {results['white_nodes']}")
    output.append(f"Black Nodes: {results['black_nodes']}")
    output.append(f"White Nodes per Move: {results['white_nodes_per_move']}")
    output.append(f"Black Nodes per Move: {results['black_nodes_per_move']}")
    output.append(f"White Time per Move: {results['white_time_per_move']}")
    output.append(f"Black Time per Move: {results['black_time_per_move']}")
    output.append(f"White Captures: {results['white_captures']}")
    output.append(f"Black Captures: {results['black_captures']}")
    output.append(f"Total Moves Til Win: {results['total_moves']}")
    output.append("")  # blank line

    text = "\n".join(output)

    # print to console
    print(text)

    # optionally write to file
    if file:
        file.write(text + "\n")

def board_to_str(board):
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    return "\n".join("".join(chars[board[r][c]] for c in range(8)) for r in range(8))


if __name__ == '__main__':
    main()
