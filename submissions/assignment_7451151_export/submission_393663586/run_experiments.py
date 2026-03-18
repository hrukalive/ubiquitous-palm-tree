from itertools import combinations
import numpy as np
from breakthrough import play_game, Breakthrough
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent, RandomAgent
from simplified_state import simplify_state, display_simplified_state

# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Chase Behrens
# YOUR WPI ID: 901008229
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

def display_results(res, agents):
    print(f"{res['total_moves']} Moves Played") 
    winner = 0 if res['winner'] == "white" else 1
    print(f"{agents[winner].name} Wins")
    print()
    display_simplified_state(simplify_state(res['final_state']))
    print("                        |   White   |   Black   ")
    print(f"               Captures | {res['white_captures']:9} | {res['black_captures']:9}")
    print(f"   Total Nodes Expanded | {res['white_nodes']:9} | {res['black_nodes']:9}")
    print(f"Nodes Expanded Per Move | {res['white_nodes_per_move']:9.3f} | {res['black_nodes_per_move']:9.3f}")
    print(f"          Time Per Move | {res['white_time_per_move']:9.3f} | {res['black_time_per_move']:9.3f}")
    print()

def run_match(agent1, agent2, display=False): 
    res1 = play_game(agent1, agent2, max_moves=400, progress=True, display=display)
    res2 = play_game(agent2, agent1, max_moves=400, progress=True, display=display)
    print("=================================================================")
    print(f"Game 1 - White: {res1['white_name']} | Black: {res1['black_name']}")
    display_results(res1, [agent1, agent2])
    print(f"Game 2 - White: {res2['white_name']} | Black: {res2['black_name']}")
    display_results(res2, [agent2, agent1])
    winner1 = 1 if res1['winner'] == "white" else -1
    winner2 = 1 if res2['winner'] == "black" else -1
    match (winner1 + winner2):
        case 0:
            print("Final Outcome: Draw")
        case 2:
            print(f"Final Outcome: {agent1.name} Wins")
        case -2:
            print(f"Final Outcome: {agent2.name} Wins") 
    print("=================================================================")

from breakthrough import offensive_eval_1, defensive_eval_1, \
                         offensive_eval_2, defensive_eval_2, \
                         offensive_eval_3, defensive_eval_3, \
                         combined_eval
from evaluators import evaluator_1, evaluator_2, evaluator_3, evaluator_4

def main():
    agents = [
        MinimaxAgent("Offensive1", 3, eval_fn=offensive_eval_1),
        AlphaBetaAgent("Offensive2", 4, eval_fn=offensive_eval_2),
        AlphaBetaAgent("Offensive3", 4, eval_fn=offensive_eval_3),
        AlphaBetaAgent("Defensive1", 4, eval_fn=defensive_eval_1), 
        AlphaBetaAgent("Defensive2", 4, eval_fn=defensive_eval_2), 
        AlphaBetaAgent("Defensive3", 4, eval_fn=defensive_eval_3),
        AlphaBetaAgent("Combo", 4, eval_fn=combined_eval), 
        AlphaBetaAgent("Evaluator1", 4, eval_fn=evaluator_1), 
        #AlphaBetaAgent("Evaluator2", 4, eval_fn=evaluator_2), To slow for my computer
        AlphaBetaAgent("Evaluator3", 4, eval_fn=evaluator_3), 
        AlphaBetaAgent("Evaluator4", 4, eval_fn=evaluator_4), 
    ]

    for agent1, agent2 in combinations(agents, 2):
        run_match(agent1, agent2, display=False)

if __name__ == '__main__':
    main()
