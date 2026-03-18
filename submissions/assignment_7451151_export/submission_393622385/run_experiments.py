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
# YOUR NAME: Brycen Pina
# YOUR WPI ID: 883953549
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

    # Agents
    # AlphaBeta agents.
    abd1 = AlphaBetaAgent("AB-Deff-1", 2, eval_fn=defensive_eval_1)
    abd2 = AlphaBetaAgent("AB-Deff-2", 2, eval_fn=defensive_eval_2)
    abo1 = AlphaBetaAgent("AB-Off-1", 2, eval_fn=offensive_eval_1)
    abo2 = AlphaBetaAgent("AB-Off-2", 2, eval_fn=offensive_eval_2)

    # Minimax agents.
    mmo1 = MinimaxAgent("MM-Off-1", 2, eval_fn=offensive_eval_1)

    # Match ups
    matchups = (
        (mmo1, abo1),
        (abo2, abd1),
        (abd2, abo1),
        (abo2, abo1),
        (abd2, abd1),
        (abo2, abd2)
    )

    for i, (p1, p2) in enumerate(matchups):
        match = play_game(p1, p2, max_moves=400, display=True, progress=True)
        print(f" -- Match#: {i + 1} --")
        print(f"Winning player: {match['winner']}.")
        print(f"White player nodes expanded: {match['white_nodes']}.")
        print(f"Black player nodes expanded: {match['black_nodes']}.")
        print(f"White player average number of nodes expanded per move: {match['white_nodes_per_move']}. avr. time: {match['white_time_per_move']}.")
        print(f"Black player average number of nodes expanded per move: {match['black_nodes_per_move']}. avr. time: {match['black_time_per_move']}.")
        input("Press enter to continue match making.") # Allow for seeing results.

if __name__ == '__main__':
    main()
