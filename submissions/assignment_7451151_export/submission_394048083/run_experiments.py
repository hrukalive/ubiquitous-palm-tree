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
# YOUR NAME: Zoya Ahmad
# YOUR WPI ID: 997076943 zahmad
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm
# Perform the necessary experiments here to generate data required by the report.

def main():
    matchups = [
        (MinimaxAgent("MM-Off1", 3, offensive_eval_1),
         AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),

        (AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AB-Def1", 4, defensive_eval_1)),

         (AlphaBetaAgent("AB-Def2", 4, defensive_eval_2),
          AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),

        (AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),

        (AlphaBetaAgent("AB-Def2", 4, defensive_eval_2),
         AlphaBetaAgent("AB-Def1", 4, defensive_eval_1)),

        (AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         AlphaBetaAgent("AB-Def2", 4, defensive_eval_2))]
    for white, black in matchups:
        result = play_game(white, black, display=False)
        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
