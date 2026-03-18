import json
import os
import random
import time

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
# YOUR NAME: Nick Smith
# YOUR WPI ID: 901010108
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
    ...  # YOUR EXPERIMENTS HERE

    results = {}
    num_tests = 5
    
    experiments = [
        {
            "name": "Minimax (Offensive 1) vs Alpha-Beta (Offensive 1)",
            "white": MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },
        {
            "name": "Alpha-Beta (Offensive 2) vs Alpha-Beta (Defensive 1)",
            "white": AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        },
        {
            "name": "Alpha-Beta (Defensive 2) vs Alpha-Beta (Offensive 1)",
            "white": AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },
        {
            "name": "Alpha-Beta (Offensive 2) vs Alpha-Beta (Offensive 1)",
            "white": AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1),
        },
        {
            "name": "Alpha-Beta (Defensive 2) vs Alpha-Beta (Defensive 1)",
            "white": AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2),
            "black": AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1),
        },
        {
            "name": "Minimax (Offensive 2) vs Minimax (Defensive 2)",
            "white": MinimaxAgent("Minimax Off2", depth=3, eval_fn=offensive_eval_2),
            "black": MinimaxAgent("Minimax Def2", depth=3, eval_fn=defensive_eval_2),
        }
    ]

    base_time = time.time()
    for exp in experiments:
        print(f"--- Starting Experiment: {exp['name']} ---")
        exp_name = exp['name']
        results[exp_name] = {
            "individual_results": [],
            "summary": {}
        }

        exp_time = time.time()
        for test_num in range(num_tests):
            print(f"Running Test {test_num + 1}/{num_tests}")
            
            # Refresh agents for a fresh start
            w_agent = exp['white']
            b_agent = exp['black']
            w_agent.reset()
            b_agent.reset()

            # Play the game
            result = play_game(w_agent, b_agent, max_moves=400, progress=False)

            formatted_result = {
                "test_num": test_num + 1,
                "winner": result["winner"],
                "total_moves": result["total_moves"],
                "white_agent": result["white_name"],
                "black_agent": result["black_name"],
                "white_total_nodes": result["white_nodes"],
                "black_total_nodes": result["black_nodes"],
                "white_nodes_per_move": result["white_nodes_per_move"],
                "black_nodes_per_move": result["black_nodes_per_move"],
                "white_time_per_move": result["white_time_per_move"],
                "black_time_per_move": result["black_time_per_move"],
                "white_captures": result["white_captures"],
                "black_captures": result["black_captures"],
            }

            results[exp_name]["individual_results"].append(formatted_result)
            #print(f"Completed {exp_name} - Test {test_num + 1}/{num_tests}")
        
        # Create a summary for the experiment
        tests = results[exp_name]["individual_results"]
        white_wins = sum(1 for t in tests if t["winner"] == "white")
        black_wins = sum(1 for t in tests if t["winner"] == "black")
        results[exp_name]["summary"] = {
            "white_agent": tests[0]["white_agent"],
            "black_agent": tests[0]["black_agent"],
            "white_wins": white_wins,
            "black_wins": black_wins,
            "avg_total_moves": sum(t["total_moves"] for t in tests) / num_tests,
            "avg_white_total_nodes": sum(t["white_total_nodes"] for t in tests) / num_tests,
            "avg_black_total_nodes": sum(t["black_total_nodes"] for t in tests) / num_tests,
            "avg_white_nodes_per_move": sum(t["white_nodes_per_move"] for t in tests) / num_tests,
            "avg_black_nodes_per_move": sum(t["black_nodes_per_move"] for t in tests) / num_tests,
            "avg_white_time_per_move": sum(t["white_time_per_move"] for t in tests) / num_tests,
            "avg_black_time_per_move": sum(t["black_time_per_move"] for t in tests) / num_tests,
            "avg_white_captures": sum(t["white_captures"] for t in tests) / num_tests,
            "avg_black_captures": sum(t["black_captures"] for t in tests) / num_tests,
        }
        exp_time = time.time() - exp_time
        print(f"--- Finished {exp_name} in {exp_time:.2f} seconds. ---\n")
    
    base_time = time.time() - base_time
    print(f"All experiments completed in {base_time:.2f} seconds.")
    filename_full = "report.json"
    filename = "report.json"

    if os.path.exists(filename_full):
        random_suffix = random.randint(1000, 9999)
        filename_full = f"report_{random_suffix}_full.json"
        filename = f"report_{random_suffix}.json"

    with open(filename_full, "w") as f:
        json.dump(results, f, indent=4)
    
    summary_only = {}
    for exp_name, data in results.items():
        summary_only[exp_name] = data["summary"]
    with open(filename, "w") as f:
        json.dump(summary_only, f, indent=4)

    print(f"\nResults saved to {filename}")
    print(f"Full results saved to {filename_full}")

    print(f"\nGoodbye.")

if __name__ == '__main__':
    main()
