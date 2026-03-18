import json

from breakthrough import defensive_eval_1, offensive_eval_1
from breakthrough import defensive_eval_2, offensive_eval_2
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
# YOUR NAME: Connor White
# YOUR WPI ID: 141158538
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

import pandas as pd


def main():
    matchups = [
        {
            'match': '1 Minimax(Offensive Evaluation 1) vs Alpha-beta(Offensive Evaluation 1)',
            'w_agent': MinimaxAgent("Minimax (off 1)", depth=3, eval_fn=offensive_eval_1),
            'b_agent': AlphaBetaAgent("Alpha Beta (off 1)", depth=3, eval_fn=offensive_eval_1),
        },

        {
            'match': '2 Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 1)',
            'w_agent': AlphaBetaAgent("Alpha Beta (off 2)", depth=3, eval_fn=offensive_eval_2),
            'b_agent': AlphaBetaAgent("Alpha Beta (def 1)", depth=3, eval_fn=defensive_eval_1),
        },

        {
            'match': '3 Alpha-beta(Defensive Evaluation 2) vs Alpha-beta(Offensive Evaluation 1)',
            'w_agent': AlphaBetaAgent("Alpha Beta (def 2)", depth=3, eval_fn=defensive_eval_2),
            'b_agent': AlphaBetaAgent("Alpha Beta (off 1)", depth=3, eval_fn=offensive_eval_1),
        },

        {
            'match': '4 Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Offensive Evaluation 1)',
            'w_agent': AlphaBetaAgent("Alpha Beta (off 2)", depth=3, eval_fn=offensive_eval_2),
            'b_agent': AlphaBetaAgent("Alpha Beta (off 1)", depth=3, eval_fn=offensive_eval_1),
        },

        {
            'match': '5 Alpha-beta(Defensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 1)',
            'w_agent': AlphaBetaAgent("Alpha Beta (def 2)", depth=3, eval_fn=defensive_eval_2),
            'b_agent': AlphaBetaAgent("Alpha Beta (def 1)", depth=3, eval_fn=defensive_eval_1),
        },

        {
            'match': '6 Alpha-beta(Offensive Evaluation 2) vs Alpha-beta(Defensive Evaluation 2)',
            'w_agent': AlphaBetaAgent("Alpha Beta (off 2)", depth=3, eval_fn=offensive_eval_2),
            'b_agent': AlphaBetaAgent("Alpha Beta (def 2)", depth=3, eval_fn=defensive_eval_2),
        },
    ]

    results = []

    for m in matchups:
        print("________________________________________", m['match'], "\n")
        m['w_agent'].reset()
        m['b_agent'].reset()
        stats = play_game(m['w_agent'], m['b_agent'], max_moves=400, progress=True, display=False)
        stats['match'] = m['match']
        results.append(stats)

    df = pd.DataFrame(results)

    report_columns = ['match', 'winner', 'total_moves', 'white_nodes', 'black_nodes',
                      'white_time_per_move', 'black_time_per_move',
                      'white_captures', 'black_captures',]
    df_report = df[report_columns]
    print(df_report)
    df_report.to_csv("breakthrough_results.csv", index=False)

    # print(results)


if __name__ == '__main__':
    main()
