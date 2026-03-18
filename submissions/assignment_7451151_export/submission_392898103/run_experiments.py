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
# YOUR NAME: Gor Arzanyan
# YOUR WPI ID: 901058692
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
# Perform the necessary experiments here to generate data required by the report.


def main():
    # Helper to create agents easily
    def get_agent(type_str, name_prefix):
        if type_str == "Off1": return AlphaBetaAgent(f"{name_prefix} Off1", 3, offensive_eval_1)
        if type_str == "Def1": return AlphaBetaAgent(f"{name_prefix} Def1", 3, defensive_eval_1)
        if type_str == "Off2": return AlphaBetaAgent(f"{name_prefix} Off2", 3, offensive_eval_2)
        if type_str == "Def2": return AlphaBetaAgent(f"{name_prefix} Def2", 3, defensive_eval_2)

    matchup_configs = [
        ("Off1", "Off1"), # 1) Off1 vs Off1
        ("Off2", "Def1"), # 2) Off2 vs Def1
        ("Def2", "Off1"), # 3) Def2 vs Off1
        ("Off2", "Off1"), # 4) Off2 vs Off1
        ("Def2", "Def1"), # 5) Def2 vs Def1
        ("Off2", "Def2")  # 6) Off2 vs Def2
    ]



    for i, (w_type, b_type) in enumerate(matchup_configs, 1):
        white = get_agent(w_type, "White")
        black = get_agent(b_type, "Black")
        
        print(f"\n{'='*25} EXPERIMENT {i} {'='*25}")
        print(f"Matchup: {white.name} (White) vs {black.name} (Black)")
        
        results = play_game(white, black, max_moves=400, display=False, progress=True)

        # B. Total Nodes Expanded
        print("\nB. TOTAL NODES EXPANDED:")
        print(f"   White: {results['white_nodes']}")
        print(f"   Black: {results['black_nodes']}")

        # C. Averages
        print("\nC. AVERAGES PER MOVE:")
        print(f"   White: {results['white_nodes_per_move']:.2f} nodes, {results['white_time_per_move']:.4f}s")
        print(f"   Black: {results['black_nodes_per_move']:.2f} nodes, {results['black_time_per_move']:.4f}s")

        # D. Game Summary
        print("\nD. GAMEPLAY SUMMARY:")
        print(f"   Winner: {results['winner'].upper()}")
        print(f"   White captures: {results['white_captures']}")
        print(f"   Black captures: {results['black_captures']}")
        print(f"   Total moves: {results['total_moves']}")
        print("-" * 65)


if __name__ == '__main__':
    main()
