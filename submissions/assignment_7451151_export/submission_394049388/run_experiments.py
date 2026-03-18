from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
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
# YOUR NAME: Nicholas Calcasola
# YOUR WPI ID: 901008099
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


# Perform the necessary experiments here to generate data required by the report.


"""
Part 8: This is just running through the matchups described in the report
and printing out the stats in a nice format.

1. How do you implement Breakthrough as a game?
I implemented Breakthrouugh fully obesrvable, zero-sum game in an 8x8 grid
with a state tracking positions turn order and capture counts. Plyaers pieces 
can move forward into empty spaces, or diagonally into empty spaces or captures. 
The game ends when a piece reaches the end of the board, or when all pieces are captured.

2. Quickly go through the two designs of your evaluation functions.
My offensive eval encourages aggressive play by calcuating how many
rows forward each piece is and applies a bonus mutliplier. While my custom
defensive promits building a back wall by awarding points for pieces staying on the back
row.

3. Summarize the implemented alpha-beta search.
My AB search looks ahead to a specific depth limit, evaluating the 
state to choose best possible move. Using ab pruning to skip branches
and drastically improves the minimax search. 

4. How did you perform the necessary experiments.
I wrote a automated script that prints out the results of each matchup
for the specific hueristics. The code below goes through each set matchup
tracking all the metrics needed from the results given in the play_game 
function written by the professor in a nice format. 

"""


def run_matchup(matchup_id, agent1_class, eval1, agent2_class, eval2):
    print(f"\n{'='*60}")
    print(f"MATCHUP {matchup_id}")
    print(f"{'='*60}")

    # Initialize Agents
    white = agent1_class(name="White_Agent", depth=3, eval_fn=eval1)
    black = agent2_class(name="Black_Agent", depth=3, eval_fn=eval2)

    results = play_game(white, black, max_moves=400, display=False, progress=True)
    final_state = results["final_state"]

    # Print the stats
    print("\nReport Stats")
    print(f"A Winner: {results['winner'].upper()}")
    print("\n Final Board State:")
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    board_output = "\n".join(
        "    " + "".join(chars[final_state["board"][r][c]] for c in range(8))
        for r in range(8)
    )
    print(board_output)

    print(f"\nB Total Nodes Expanded:")
    print(f"White: {results['white_nodes']}")
    print(f"Black: {results['black_nodes']}")

    print(f"\nC Averages:")
    print(
        f"White: {results['white_nodes_per_move']:.1f} nodes/move | {results['white_time_per_move']:.4f} sec/move"
    )
    print(
        f"Black: {results['black_nodes_per_move']:.1f} nodes/move | {results['black_time_per_move']:.4f} sec/move"
    )

    print(f"\nD Game Details:")
    print(f"White Captures: {results['white_captures']}")
    print(f"Black Captures: {results['black_captures']}")
    print(f"Total Moves: {results['total_moves']}")


def main():
    print("Starting Experiments")

    # 1) Minimax (Off 1) vs Alpha-beta (Off 1)
    run_matchup(
        "1) Minimax (Off 1) vs Alpha-beta (Off 1)",
        MinimaxAgent,
        offensive_eval_1,
        AlphaBetaAgent,
        offensive_eval_1,
    )

    # 2) Alpha-beta (Off 2) vs Alpha-beta (Def 1)
    run_matchup(
        "2) Alpha-beta (Off 2) vs Alpha-beta (Def 1)",
        AlphaBetaAgent,
        offensive_eval_2,
        AlphaBetaAgent,
        defensive_eval_1,
    )

    # 3) Alpha-beta (Def 2) vs Alpha-beta (Off 1)
    run_matchup(
        "3) Alpha-beta (Def 2) vs Alpha-beta (Off 1)",
        AlphaBetaAgent,
        defensive_eval_2,
        AlphaBetaAgent,
        offensive_eval_1,
    )

    # 4) Alpha-beta (Off 2) vs Alpha-beta (Off 1)
    run_matchup(
        "4) Alpha-beta (Off 2) vs Alpha-beta (Off 1)",
        AlphaBetaAgent,
        offensive_eval_2,
        AlphaBetaAgent,
        offensive_eval_1,
    )

    # 5) Alpha-beta (Def 2) vs Alpha-beta (Def 1)
    run_matchup(
        "5) Alpha-beta (Def 2) vs Alpha-beta (Def 1)",
        AlphaBetaAgent,
        defensive_eval_2,
        AlphaBetaAgent,
        defensive_eval_1,
    )

    # 6) Alpha-beta (Off 2) vs Alpha-beta (Def 2)
    run_matchup(
        "6) Alpha-beta (Off 2) vs Alpha-beta (Def 2)",
        AlphaBetaAgent,
        offensive_eval_2,
        AlphaBetaAgent,
        defensive_eval_2,
    )


if __name__ == "__main__":
    main()
