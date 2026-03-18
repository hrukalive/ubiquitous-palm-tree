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
# YOUR NAME: Antoine Pham
# YOUR WPI ID: 9001008366
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

def print_results(matchup_num, description, result):
    print("=" * 60)
    print(f"Matchup {matchup_num}: {description}")
    print("=" * 60)
    print(f"Winner: {result['winner']}")
    print(f"Total moves: {result['total_moves']}")
    print(f"White nodes total:        {result['white_nodes']}")
    print(f"Black nodes total:        {result['black_nodes']}")
    print(f"White avg nodes/move:     {result['white_nodes_per_move']:.1f}")
    print(f"Black avg nodes/move:     {result['black_nodes_per_move']:.1f}")
    print(f"White avg time/move (s):  {result['white_time_per_move']:.4f}")
    print(f"Black avg time/move (s):  {result['black_time_per_move']:.4f}")
    print(f"White captures:           {result['white_captures']}")
    print(f"Black captures:           {result['black_captures']}")
    print()


def main():
    # Matchup 1: Minimax(Off1) vs AlphaBeta(Off1)
    print("Running Matchup 1...")
    result = play_game(
        MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        display=True, progress=True
    )
    print_results(1, "Minimax(OffEval1) [W] vs AlphaBeta(OffEval1) [B]", result)

    # Matchup 2: AlphaBeta(Off2) vs AlphaBeta(Def1)
    print("Running Matchup 2...")
    result = play_game(
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        display=True, progress=True
    )
    print_results(2, "AlphaBeta(OffEval2) [W] vs AlphaBeta(DefEval1) [B]", result)

    # Matchup 3: AlphaBeta(Def2) vs AlphaBeta(Off1)
    print("Running Matchup 3...")
    result = play_game(
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        display=True, progress=True
    )
    print_results(3, "AlphaBeta(DefEval2) [W] vs AlphaBeta(OffEval1) [B]", result)

    # Matchup 4: AlphaBeta(Off2) vs AlphaBeta(Off1)
    print("Running Matchup 4...")
    result = play_game(
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        display=True, progress=True
    )
    print_results(4, "AlphaBeta(OffEval2) [W] vs AlphaBeta(OffEval1) [B]", result)

    # Matchup 5: AlphaBeta(Def2) vs AlphaBeta(Def1)
    print("Running Matchup 5...")
    result = play_game(
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        display=True, progress=True
    )
    print_results(5, "AlphaBeta(DefEval2) [W] vs AlphaBeta(DefEval1) [B]", result)

    # Matchup 6: AlphaBeta(Off2) vs AlphaBeta(Def2)
    print("Running Matchup 6...")
    result = play_game(
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
        display=True, progress=True
    )
    print_results(6, "AlphaBeta(OffEval2) [W] vs AlphaBeta(DefEval2) [B]", result)


if __name__ == '__main__':
    main()
