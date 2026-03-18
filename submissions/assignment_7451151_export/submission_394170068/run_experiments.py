import json
from itertools import combinations
from tqdm import tqdm
from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
# from breakthrough import gmo_agent
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
# YOUR NAME: Zachary Serocki
# YOUR WPI ID: 901008740
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
def round_robin(strategies,search_depth, max_moves = 400, display = False, progress = True):
    r = 2
    combos = combinations(strategies, r)
    accumulated_results = {}
    
    
    for combo in combos:
        print(f"running: {combo[0].__name__} v {combo[1].__name__}")
        agent_0 = AlphaBetaAgent(combo[0].__name__, depth=search_depth, eval_fn=combo[0])
        agent_1 = AlphaBetaAgent(combo[1].__name__, depth=search_depth, eval_fn=combo[1])
        results = play_game(agent_0, agent_1, max_moves=max_moves, display=display, progress=progress)
        key = combo[0].__name__ + " v " + combo[1].__name__
        accumulated_results[key] = results
        print(f"running: {combo[1].__name__} v {combo[0].__name__}")
        agent_0 = AlphaBetaAgent(combo[0].__name__, depth=search_depth, eval_fn=combo[0])
        agent_1 = AlphaBetaAgent(combo[1].__name__, depth=search_depth, eval_fn=combo[1])
        results = play_game(agent_1, agent_0, max_moves=max_moves, display=display, progress=progress)
        key = combo[1].__name__ + " v " + combo[0].__name__
        accumulated_results[key] = results
        
    print(f"running: {strategies[0].__name__} v {strategies[1].__name__}")
    agent_0 = MinimaxAgent(strategies[0].__name__, depth=search_depth, eval_fn=strategies[0])
    agent_1 = AlphaBetaAgent(strategies[0].__name__, depth=search_depth, eval_fn=strategies[0])
    
    results = play_game(agent_0, agent_1, max_moves=max_moves, display=display, progress=progress)
    key = strategies[0].__name__ + "_MiniMax v " + strategies[0].__name__ + "_AlphaBeta"
    accumulated_results[key] = results
    
    print(f"running: {strategies[0].__name__} v {strategies[0].__name__}")
    agent_0 = AlphaBetaAgent(strategies[0].__name__, depth=search_depth, eval_fn=strategies[0])
    agent_1 = MinimaxAgent(strategies[0].__name__, depth=search_depth, eval_fn=strategies[0])
    
    results = play_game(agent_0, agent_1, max_moves=max_moves, display=display, progress=progress)
    key = strategies[0].__name__ + "_AlphaBeta v " + strategies[0].__name__ + "_MiniMax"
    accumulated_results[key] = results
    with open("data/round_robin_results2.json", "w") as f:
        json.dump(accumulated_results, f)
            
            
    
def main():
    strats = [offensive_eval_1,defensive_eval_1,offensive_eval_2,defensive_eval_2]

    round_robin(strats,search_depth=4)

if __name__ == '__main__':
    main()
