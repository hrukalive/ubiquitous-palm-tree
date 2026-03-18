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
# YOUR NAME: Nicole Guan
# YOUR WPI ID: 901031192
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


def run_matchup(matchup_num, white_agent, black_agent):
    print(f"\n{'='*20} MATCHUP {matchup_num} {'='*20}")
    print(f"White: {white_agent.name} vs Black: {black_agent.name}")
    
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    
    print(f"\nMatchup {matchup_num} Results:")
    print(json.dumps(results, indent=4))
    return results

def main():
    d = 3 
    #run_matchup(1, 
    #            MinimaxAgent("Minimax Off1", depth=d, eval_fn=offensive_eval_1),
    #            AlphaBetaAgent("AlphaBeta Off1", depth=d, eval_fn=offensive_eval_1))
    #run_matchup(2, 
    #            AlphaBetaAgent("AlphaBeta Off1", depth=d, eval_fn=offensive_eval_1),
    #            AlphaBetaAgent("AlphaBeta Def1", depth=d, eval_fn=defensive_eval_1))
    #run_matchup(3, 
    #           AlphaBetaAgent("AlphaBeta Off2", depth=d, eval_fn=offensive_eval_2),
    #           AlphaBetaAgent("AlphaBeta Def2", depth=d, eval_fn=defensive_eval_2))
    #run_matchup(4, 
    #            AlphaBetaAgent("AlphaBeta Off2", depth=d, eval_fn=offensive_eval_2),
    #            AlphaBetaAgent("AlphaBeta Off1", depth=d, eval_fn=offensive_eval_1))
    #run_matchup(5, 
    #            AlphaBetaAgent("AlphaBeta Def2", depth=d, eval_fn=defensive_eval_2),
    #            AlphaBetaAgent("AlphaBeta Def1", depth=d, eval_fn=defensive_eval_1))
    run_matchup(6, 
                AlphaBetaAgent("AlphaBeta Off2", depth=d, eval_fn=offensive_eval_2),
                AlphaBetaAgent("AlphaBeta Def1", depth=d, eval_fn=defensive_eval_1))

if __name__ == '__main__':
    main()