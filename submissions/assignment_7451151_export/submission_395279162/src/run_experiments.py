import json

from breakthrough import Breakthrough, offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
from tqdm import tqdm

# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Marc Godbout-Chouinard
# YOUR WPI ID: 901012575
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
    matchups = [
        ("Minimax Off1", MinimaxAgent("MM-Off1", 3, offensive_eval_1),
         "AB Off1", AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),
        ("AB Off2", AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         "AB Def1", AlphaBetaAgent("AB-Def1", 4, defensive_eval_1)),
        ("AB Def2", AlphaBetaAgent("AB-Def2", 4, defensive_eval_2),
         "AB Off1", AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),
        ("AB Off2", AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         "AB Off1", AlphaBetaAgent("AB-Off1", 4, offensive_eval_1)),
        ("AB Def2", AlphaBetaAgent("AB-Def2", 4, defensive_eval_2),
         "AB Def1", AlphaBetaAgent("AB-Def1", 4, defensive_eval_1)),
        ("AB Off2", AlphaBetaAgent("AB-Off2", 4, offensive_eval_2),
         "AB Def2", AlphaBetaAgent("AB-Def2", 4, defensive_eval_2)),
    ]
    
    game = Breakthrough()
    all_results = []
    
    for i, (wname, wagent, bname, bagent) in enumerate(matchups, 1):
        print(f"Matchup {i}: {wname} (White) vs {bname} (Black)")

        state = game.initial_state()
        move_count = 0
        pbar = tqdm(total=400, desc="Game in progress", ncols=100)
        
        while True:
            if state["to_move"] == "WHITE":
                move = wagent.select_move(game, state)
            else:
                move = bagent.select_move(game, state)
            
            state = game.result(state, move)
            move_count += 1
            pbar.update()
            
            if game.terminal_test(state) or move_count >= 400:
                if move_count < 400:
                    winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
                else:
                    winner = None
                break
        
        pbar.close()
        
        white_nodes = sum(wagent.nodes_per_move)
        black_nodes = sum(bagent.nodes_per_move)
        white_time_per_move = sum(wagent.time_per_move) / len(wagent.time_per_move)
        black_time_per_move = sum(bagent.time_per_move) / len(bagent.time_per_move)
        white_nodes_per_move = white_nodes / len(wagent.nodes_per_move)
        black_nodes_per_move = black_nodes / len(bagent.nodes_per_move)
        white_captures = state["captures"]["WHITE"]
        black_captures = state["captures"]["BLACK"]
        
        result = {
            'winner': 'white' if winner == "WHITE" else 'black' if winner == "BLACK" else None,
            'white_name': wagent.name,
            'black_name': bagent.name,
            'total_moves': move_count,
            'white_nodes': white_nodes,
            'black_nodes': black_nodes,
            'white_nodes_per_move': white_nodes_per_move,
            'black_nodes_per_move': black_nodes_per_move,
            'white_time_per_move': white_time_per_move,
            'black_time_per_move': black_time_per_move,
            'white_captures': white_captures,
            'black_captures': black_captures,
            'final_state': state
        }
        
        print(f"\nWinner: {result['winner']}")
        print(f"Total moves: {result['total_moves']}")
        print(f"White captures: {result['white_captures']}, Black captures: {result['black_captures']}")
        print(f"White nodes: {result['white_nodes']}, Black nodes: {result['black_nodes']}")
        print(f"White avg nodes/move: {result['white_nodes_per_move']:.1f}")
        print(f"Black avg nodes/move: {result['black_nodes_per_move']:.1f}")
        print(f"White avg time/move: {result['white_time_per_move']:.4f}s")
        print(f"Black avg time/move: {result['black_time_per_move']:.4f}s")
        
        print(f"\nFinal Board")
        game.display(result['final_state'])
        
        all_results.append(result)

        wagent.reset()
        bagent.reset()
    
    print("Summary Table")

    print(f"{'Match':<8} {'White':<20} {'Black':<20} {'Winner':<8} {'Moves':<6} {'W Cap':<6} {'B Cap':<6}")
    
    for i, result in enumerate(all_results, 1):
        print(f"{i:<8} {result['white_name']:<20} {result['black_name']:<20} "
              f"{result['winner']:<8} {result['total_moves']:<6} "
              f"{result['white_captures']:<6} {result['black_captures']:<6}")
    
    print("Report Statistics")
    
    for i, result in enumerate(all_results, 1):
        print(f"\nMatchup {i}:")
        print(f"  White: {result['white_name']} | Black: {result['black_name']}")
        print(f"  Winner: {result['winner']} | Total Moves: {result['total_moves']}")
        print(f"  Captures - White: {result['white_captures']}, Black: {result['black_captures']}")
        print(f"  Nodes Expanded - White: {result['white_nodes']:,}, Black: {result['black_nodes']:,}")
        print(f"  Nodes/Move - White: {result['white_nodes_per_move']:.1f}, Black: {result['black_nodes_per_move']:.1f}")
        print(f"  Time/Move - White: {result['white_time_per_move']:.4f}s, Black: {result['black_time_per_move']:.4f}s")


if __name__ == '__main__':
    main()
