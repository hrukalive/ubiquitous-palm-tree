import json
from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                                   _             _
#  |_   _|                                 | |           | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Aditya Manoj Krishna
# YOUR WPI ID: amkrishna@wpi.edu

def main():
    # Define the matchups as requested
    # Tuple format: (White Agent Class, White Eval, Black Agent Class, Black Eval, Label)
    matchups = [
        (MinimaxAgent, offensive_eval_1, AlphaBetaAgent, offensive_eval_1, "1) Minimax (Off1) vs Alpha-beta (Off1)"),
        (AlphaBetaAgent, offensive_eval_2, AlphaBetaAgent, defensive_eval_1, "2) Alpha-beta (Off2) vs Alpha-beta (Def1)"),
        (AlphaBetaAgent, defensive_eval_2, AlphaBetaAgent, offensive_eval_1, "3) Alpha-beta (Def2) vs Alpha-beta (Off1)"),
        (AlphaBetaAgent, offensive_eval_2, AlphaBetaAgent, offensive_eval_1, "4) Alpha-beta (Off2) vs Alpha-beta (Off1)"),
        (AlphaBetaAgent, defensive_eval_2, AlphaBetaAgent, defensive_eval_1, "5) Alpha-beta (Def2) vs Alpha-beta (Def1)"),
        (AlphaBetaAgent, offensive_eval_2, AlphaBetaAgent, defensive_eval_2, "6) Alpha-beta (Off2) vs Alpha-beta (Def2)")
    ]

    experiment_results = []

    print("Starting Breakthrough Experiments...\n")

    for white_cls, white_eval, black_cls, black_eval, label in matchups:
        print(f"Running Matchup {label}...")
        
        # Initialize Agents
        # Note: We use depth=3 for a balance between performance and search quality
        white_agent = white_cls(name="White", depth=3, eval_fn=white_eval)
        black_agent = black_cls(name="Black", depth=3, eval_fn=black_eval)

        # Play the game
        # display=False to speed up execution; progress=True to see tqdm bar
        result = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
        
        # Add the label to the result for identification
        result['matchup_description'] = label
        experiment_results.append(result)

        print(f"Winner: {result['winner']}")
        print(f"Total Moves: {result['total_moves']}")
        print(f"Nodes (White): {result['white_nodes']} | Nodes (Black): {result['black_nodes']}")
        print("-" * 50)

    # Optional: Save results to a JSON file for your report analysis
    with open('experiment_data.json', 'w') as f:
        json.dump(experiment_results, f, indent=4)
    
    print("\nExperiments complete. Data saved to experiment_data.json.")


if __name__ == '__main__':
    main()