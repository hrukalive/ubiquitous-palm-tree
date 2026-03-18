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
# YOUR NAME: Ryan Zhang
# YOUR WPI ID: 901010248
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

def run_matchup(white_agent, black_agent, max_moves=400):
    print(f"\n=== {white_agent.name} (White) vs {black_agent.name} (Black) ===")
    results = play_game(
        white_agent,
        black_agent,
        max_moves=max_moves,
        display=True,
        progress=False
    )
    print(results)
    return results

def main():
    all_results = []
    #1)Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
    white = MinimaxAgent("Minimax Off1", eval_fn=offensive_eval_1)
    black = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black))

    #2)Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    white = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", eval_fn=defensive_eval_1)
    all_results.append(run_matchup(white, black))

    #3)Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    white = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black))

    #4)Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
    white = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", eval_fn=offensive_eval_1)
    all_results.append(run_matchup(white, black))

    #5)Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
    white = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", eval_fn=defensive_eval_1)
    all_results.append(run_matchup(white, black))

    #6)Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
    white = AlphaBetaAgent("AlphaBeta Off2", eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def2", eval_fn=defensive_eval_2)
    all_results.append(run_matchup(white, black))

    #Save results to JSON
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\n=== ALL RESULTS SAVED TO experiment_results.json ===")


if __name__ == '__main__':
    main()
