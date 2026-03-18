import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game, Breakthrough
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
# YOUR NAME: Joshua Gifford
# YOUR WPI ID: 901016700
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

# Perform the necessary experiments here to generate data required by the report.
def main():
    win_count = 0
    num_moves = 0
    white_agents = [(MinimaxAgent, offensive_eval_1), #game #1
                    (AlphaBetaAgent, offensive_eval_2), #2
                    (AlphaBetaAgent, defensive_eval_2), #3
                    (AlphaBetaAgent, offensive_eval_2), #4
                    (AlphaBetaAgent, defensive_eval_2), #5
                    (AlphaBetaAgent, offensive_eval_2) #6
                    ]
    black_agents = [(AlphaBetaAgent, offensive_eval_1), #game #1
                    (AlphaBetaAgent, defensive_eval_1), #2
                    (AlphaBetaAgent, offensive_eval_1), #3
                    (AlphaBetaAgent, offensive_eval_1), #4
                    (AlphaBetaAgent, defensive_eval_1), #5
                    (AlphaBetaAgent, defensive_eval_2) #6
                    ]
    for i in range(len(white_agents)): #len(white_agents) IMPORTANT CHANGE IF WANT TO RUN ALL GAMES
        white_agent_class, white_eval_fn = white_agents[i] #grab agent and eval_fn
        black_agent_class, black_eval_fn = black_agents[i]

        white_name = f"{white_agent_class.__name__}_{white_eval_fn.__name__}" #name is agentName_evaluationFunction
        black_name = f"{black_agent_class.__name__}_{black_eval_fn.__name__}"

        d = 4 #change depth to 4 but not for minimax!
        if white_agent_class.__name__ == "MinimaxAgent":
            d = 3
        w_agent = white_agent_class(white_name, d, eval_fn=white_eval_fn) #use agent and eval_fn
        b_agent = black_agent_class(black_name, 4, eval_fn=black_eval_fn)
        res = play_game(w_agent, b_agent, max_moves=400, progress=True) #play game
        print(f"--- MATCHUP #{i + 1} REPORT ---") #results
        print(f"White Agent: {white_name}")
        print(f"Black Agent: {black_name}")

        #Final state and winner
        print(f"WINNER: {res['winner'].upper()}")
        game = Breakthrough()
        print(game.display(res['final_state'])) #shows winner (ADDED FINAL STATE to res)

        #Node expansion and timing
        print(f"{'Stat':<25} | {'White (W)':<20} | {'Black (B)':<20}")
        print("-" * 70)
        print(f"{'Total Nodes Expanded':<25} | {res['white_nodes']:<20} | {res['black_nodes']:<20}")
        print(f"{'Avg Nodes / Move':<25} | {res['white_nodes_per_move']:<20.2f} | {res['black_nodes_per_move']:<20.2f}")
        print(
            f"{'Avg Time / Move (s)':<25} | {res['white_time_per_move']:<20.4f} | {res['black_time_per_move']:<20.4f}")

        #Captures and duration
        # print(f"\nOpponent Workers Captured: White={res['white_captures']}, Black={res['black_captures']}") #given above in final state
        print(f"Total Game Moves: {res['total_moves']}")
        print("=" * 70)

if __name__ == '__main__':
    main()
