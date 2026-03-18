import json

from breakthrough import offensive_heuristic_1, defensive_heuristic_1
from breakthrough import offensive_heuristic_2, defensive_heuristic_2
from breakthrough import play_game
from breakthrough import Breakthrough
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
# YOUR NAME: Kavin Duraiarasu
# YOUR WPI ID: 901044227
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm

def print_board(state):
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    board = state['board']
    print("  0 1 2 3 4 5 6 7")
    for r in range(8):
        row = " ".join(chars[board[r][c]] for c in range(8))
        print(f"{r} {row}")


def run_and_report(matchup_num, description, white_agent, black_agent):
    """Run one matchup, capture the final board state, and print all required stats."""
    game = Breakthrough()
    state = game.initial_state()
    max_moves = 400
    move_count = 0

    from tqdm import tqdm
    pbar = tqdm(total=max_moves, desc=f"Matchup {matchup_num}", ncols=80)

    while True:
        if state["to_move"] == "WHITE":
            move = white_agent.select_move(game, state)
        else:
            move = black_agent.select_move(game, state)
        state = game.result(state, move)
        move_count += 1
        pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            break
    pbar.close()

    # Determine winner
    if move_count >= max_moves:
        winner = None
    else:
        winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"

    # Aggregate stats
    white_nodes       = sum(white_agent.nodes_per_move)
    black_nodes       = sum(black_agent.nodes_per_move)
    white_avg_nodes   = white_nodes / len(white_agent.nodes_per_move)
    black_avg_nodes   = black_nodes / len(black_agent.nodes_per_move)
    white_avg_time_ms = sum(white_agent.time_per_move) / len(white_agent.time_per_move) * 1000
    black_avg_time_ms = sum(black_agent.time_per_move) / len(black_agent.time_per_move) * 1000

    # Print report
    print()
    print("=" * 65)
    print(f"Matchup {matchup_num}: {description}")
    print("=" * 65)

    # A. Final board and winner
    print("\nA. Final Board State:")
    print_board(state)
    if winner == "WHITE":
        print(f"\n   Winner: WHITE  ({white_agent.name})")
    elif winner == "BLACK":
        print(f"\n   Winner: BLACK  ({black_agent.name})")
    else:
        print("\n   Result: No winner -- max moves reached")

    # B. Total nodes expanded
    print("\nB. Total Nodes Expanded:")
    print(f"   {white_agent.name:30s} (WHITE): {white_nodes:>10,}")
    print(f"   {black_agent.name:30s} (BLACK): {black_nodes:>10,}")

    # C. Avg nodes per move and avg time per move
    print("\nC. Avg Nodes/Move  &  Avg Time/Move:")
    print(f"   {white_agent.name:30s} (WHITE): {white_avg_nodes:>10,.1f} nodes/move   {white_avg_time_ms:>8.2f} ms/move")
    print(f"   {black_agent.name:30s} (BLACK): {black_avg_nodes:>10,.1f} nodes/move   {black_avg_time_ms:>8.2f} ms/move")

    # D. Captures and total moves
    print("\nD. Captures  &  Total Moves:")
    print(f"   WHITE captured : {state['captures']['WHITE']} opponent pieces")
    print(f"   BLACK captured : {state['captures']['BLACK']} opponent pieces")
    print(f"   Total moves    : {move_count}")
    print()

    return {
        "matchup": matchup_num,
        "description": description,
        "winner": winner,
        "white_name": white_agent.name,
        "black_name": black_agent.name,
        "white_total_nodes": white_nodes,
        "black_total_nodes": black_nodes,
        "white_avg_nodes_per_move": round(white_avg_nodes, 2),
        "black_avg_nodes_per_move": round(black_avg_nodes, 2),
        "white_avg_time_ms": round(white_avg_time_ms, 4),
        "black_avg_time_ms": round(black_avg_time_ms, 4),
        "white_captures": state['captures']['WHITE'],
        "black_captures": state['captures']['BLACK'],
        "total_moves": move_count,
    }


def main():
    all_results = []

    # 1) Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
    all_results.append(run_and_report(
        1,
        "Minimax (Off H1)  vs  Alpha-beta (Off H1)",
        MinimaxAgent("Minimax Off1",     depth=3, eval_fn=offensive_heuristic_1),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_heuristic_1),
    ))

    # 2) Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
    all_results.append(run_and_report(
        2,
        "Alpha-beta (Off H2)  vs  Alpha-beta (Def H1)",
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_heuristic_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_heuristic_1),
    ))

    # 3) Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
    all_results.append(run_and_report(
        3,
        "Alpha-beta (Def H2)  vs  Alpha-beta (Off H1)",
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_heuristic_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_heuristic_1),
    ))

    # 4) Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
    all_results.append(run_and_report(
        4,
        "Alpha-beta (Off H2)  vs  Alpha-beta (Off H1)",
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_heuristic_2),
        AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_heuristic_1),
    ))

    # 5) Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
    all_results.append(run_and_report(
        5,
        "Alpha-beta (Def H2)  vs  Alpha-beta (Def H1)",
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_heuristic_2),
        AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_heuristic_1),
    ))

    # 6) Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)
    all_results.append(run_and_report(
        6,
        "Alpha-beta (Off H2)  vs  Alpha-beta (Def H2)",
        AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_heuristic_2),
        AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_heuristic_2),
    ))

    # Save all results to JSON for easy report writing
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("All results saved to experiment_results.json")


if __name__ == '__main__':
    main()
