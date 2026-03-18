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
# YOUR NAME: Colin Truong
# YOUR WPI ID: 997075740
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

def run_matchup(white_agent, black_agent, games=1):
    results_list = []

    for i in range(games):
        white_agent.reset()
        black_agent.reset()
        
        results = play_game(
            white_agent,
            black_agent,
            max_moves=400,
            display=False,
            progress=False
        )
        results_list.append(results)

    return results_list


def summarize_results(results_list):
    total_games = len(results_list)
    white_wins = sum(1 for r in results_list if r['winner'] == 'white')
    black_wins = sum(1 for r in results_list if r['winner'] == 'black')

    avg_moves = sum(r['total_moves'] for r in results_list) / total_games
    avg_white_nodes = sum(r['white_nodes'] for r in results_list) / total_games
    avg_black_nodes = sum(r['black_nodes'] for r in results_list) / total_games
    avg_white_nodes_per_move = sum(r['white_nodes_per_move'] for r in results_list) / total_games
    avg_black_nodes_per_move = sum(r['black_nodes_per_move'] for r in results_list) / total_games
    avg_white_time = sum(r['white_time_per_move'] for r in results_list) / total_games
    avg_black_time = sum(r['black_time_per_move'] for r in results_list) / total_games
    avg_white_captures = sum(r['white_captures'] for r in results_list) / total_games
    avg_black_captures = sum(r['black_captures'] for r in results_list) / total_games

    print("\n===== SUMMARY =====")
    print(f"White wins: {white_wins}/{total_games}")
    print(f"Black wins: {black_wins}/{total_games}")
    print(f"Average moves: {avg_moves:.2f}")
    print(f"White avg total nodes: {avg_white_nodes:.0f}")
    print(f"Black avg total nodes: {avg_black_nodes:.0f}")
    print(f"White avg nodes/move: {avg_white_nodes_per_move:.2f}")
    print(f"Black avg nodes/move: {avg_black_nodes_per_move:.2f}")
    print(f"White avg time/move: {avg_white_time:.4f}s")
    print(f"Black avg time/move: {avg_black_time:.4f}s")
    print(f"White avg captures: {avg_white_captures:.2f}")
    print(f"Black avg captures: {avg_black_captures:.2f}")
    print("====================\n")

def main():
    from breakthrough_agent import AlphaBetaAgent

    DEPTH = 4
    GAMES_PER_MATCHUP = 3   # Increase to 5–10 for noise analysis

    matchups = [
        ("Off2 vs Off2",
         AlphaBetaAgent("White Off2", DEPTH, offensive_eval_2),
         AlphaBetaAgent("Black Off2", DEPTH, offensive_eval_2)),

        ("Def2 vs Def2",
         AlphaBetaAgent("White Def2", DEPTH, defensive_eval_2),
         AlphaBetaAgent("Black Def2", DEPTH, defensive_eval_2)),

        ("Off2 vs Def2",
         AlphaBetaAgent("White Off2", DEPTH, offensive_eval_2),
         AlphaBetaAgent("Black Def2", DEPTH, defensive_eval_2)),

        ("Def2 vs Off2",
         AlphaBetaAgent("White Def2", DEPTH, defensive_eval_2),
         AlphaBetaAgent("Black Off2", DEPTH, offensive_eval_2)),

        ("Off1 vs Def1",
         AlphaBetaAgent("White Off1", DEPTH, offensive_eval_1),
         AlphaBetaAgent("Black Def1", DEPTH, defensive_eval_1)),

        ("Def1 vs Off1",
         AlphaBetaAgent("White Def1", DEPTH, defensive_eval_1),
         AlphaBetaAgent("Black Off1", DEPTH, offensive_eval_1)),
    ]

    for name, white_agent, black_agent in matchups:
        print(f"\n========== {name} ==========")
        results = run_matchup(white_agent, black_agent, games=GAMES_PER_MATCHUP)
        summarize_results(results)


if __name__ == '__main__':
    main()
