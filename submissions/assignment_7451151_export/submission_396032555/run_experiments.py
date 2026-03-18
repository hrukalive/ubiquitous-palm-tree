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
# YOUR NAME: Rohan Gladson
# YOUR WPI ID: 901003651
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

def run_matchup(white_agent, black_agent, matchup_name, max_moves=400):
    # Run one full game and collect the returned statistics dictionary.
    result = play_game(
        white_agent,
        black_agent,
        max_moves=max_moves,
        display=True,
        progress=True
    )

    # Add a label so the result is easy to identify later in the report.
    result["matchup"] = matchup_name
    return result

def main():
    # Minimax should search depth 2 to 3, and alpha-beta
    # should search deeper than minimax.
    minimax_depth = 3
    alphabeta_depth = 4

    results = []

    # 1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
    white_agent = MinimaxAgent("Minimax Off1", depth=minimax_depth, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)"
    ))

    # 2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    white_agent = AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)"
    ))

    # 3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    white_agent = AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)"
    ))

    # 4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    white_agent = AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=alphabeta_depth, eval_fn=offensive_eval_1)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)"
    ))

    # 5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    white_agent = AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=alphabeta_depth, eval_fn=defensive_eval_1)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)"
    ))

    # 6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
    white_agent = AlphaBetaAgent("AlphaBeta Off2", depth=alphabeta_depth, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def2", depth=alphabeta_depth, eval_fn=defensive_eval_2)
    results.append(run_matchup(
        white_agent,
        black_agent,
        "6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)"
    ))

    # Print results clearly to the console
    for result in results:
        print("\n" + "=" * 80)
        print(result["matchup"])
        print("=" * 80)
        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
