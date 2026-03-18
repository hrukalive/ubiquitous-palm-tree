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
# YOUR NAME: John Bernard
# YOUR WPI ID: 901025640


def print_board(state):
    """Print the final board state with a labelled grid."""
    chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
    board = state['board']
    print("  0 1 2 3 4 5 6 7")
    for r in range(8):
        row_str = " ".join(chars[board[r][c]] for c in range(8))
        print(f"{r} {row_str}")
    print("  (W=White, B=Black, .=Empty)")


def run_matchup(white_agent, black_agent, max_moves=400, progress=True):
    """Run a matchup and return (result_dict, final_state)."""
    from tqdm import tqdm
    game = Breakthrough()
    state = game.initial_state()
    move_count = 0
    pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100) if progress else None
    while True:
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game, state)
        state = game.result(state, move)
        move_count += 1
        if pbar:
            pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break
    if pbar:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    result = {
        'winner': 'white' if winner == "WHITE" else 'black' if winner == "BLACK" else None,
        'white_name': white_agent.name,
        'black_name': black_agent.name,
        'total_moves': move_count,
        'white_nodes': white_nodes,
        'black_nodes': black_nodes,
        'white_nodes_per_move': white_nodes / len(white_agent.nodes_per_move),
        'black_nodes_per_move': black_nodes / len(black_agent.nodes_per_move),
        'white_time_per_move': sum(white_agent.time_per_move) / len(white_agent.time_per_move),
        'black_time_per_move': sum(black_agent.time_per_move) / len(black_agent.time_per_move),
        'white_captures': state["captures"]["WHITE"],
        'black_captures': state["captures"]["BLACK"],
    }
    return result, state


def print_result(matchup_num, description, result, final_state):
    print(f"\n{'='*60}")
    print(f"Matchup {matchup_num}: {description}")
    print(f"{'='*60}")
    print(f"Winner: {result['winner'].upper() if result['winner'] else 'Draw (max moves)'}")
    print(f"  White agent: {result['white_name']}")
    print(f"  Black agent: {result['black_name']}")
    print(f"Total moves: {result['total_moves']}")
    print(f"White - nodes expanded: {result['white_nodes']:,}  |  avg/move: {result['white_nodes_per_move']:,.1f}  |  avg time/move: {result['white_time_per_move']:.4f}s")
    print(f"Black - nodes expanded: {result['black_nodes']:,}  |  avg/move: {result['black_nodes_per_move']:,.1f}  |  avg time/move: {result['black_time_per_move']:.4f}s")
    print(f"White captures: {result['white_captures']}  |  Black captures: {result['black_captures']}")
    print("\nFinal Board State:")
    print_board(final_state)


def main():
    print("Running all 6 matchups for Breakthrough experiment...\n")

    # Matchup 1: Minimax (Off1) vs Alpha-beta (Off1)
    w1 = MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1)
    b1 = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    r1, s1 = run_matchup(w1, b1)
    print_result(1, "Minimax(Off1) [White] vs Alpha-beta(Off1) [Black]", r1, s1)

    # Matchup 2: Alpha-beta (Off2) vs Alpha-beta (Def1)
    w2 = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    b2 = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    r2, s2 = run_matchup(w2, b2)
    print_result(2, "Alpha-beta(Off2) [White] vs Alpha-beta(Def1) [Black]", r2, s2)

    # Matchup 3: Alpha-beta (Def2) vs Alpha-beta (Off1)
    w3 = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    b3 = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    r3, s3 = run_matchup(w3, b3)
    print_result(3, "Alpha-beta(Def2) [White] vs Alpha-beta(Off1) [Black]", r3, s3)

    # Matchup 4: Alpha-beta (Off2) vs Alpha-beta (Off1)
    w4 = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    b4 = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    r4, s4 = run_matchup(w4, b4)
    print_result(4, "Alpha-beta(Off2) [White] vs Alpha-beta(Off1) [Black]", r4, s4)

    # Matchup 5: Alpha-beta (Def2) vs Alpha-beta (Def1)
    w5 = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    b5 = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    r5, s5 = run_matchup(w5, b5)
    print_result(5, "Alpha-beta(Def2) [White] vs Alpha-beta(Def1) [Black]", r5, s5)

    # Matchup 6: Alpha-beta (Off2) vs Alpha-beta (Def2)
    w6 = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    b6 = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    r6, s6 = run_matchup(w6, b6)
    print_result(6, "Alpha-beta(Off2) [White] vs Alpha-beta(Def2) [Black]", r6, s6)

    # Save results to JSON
    all_results = {
        "matchup_1_minimax_off1_vs_ab_off1": r1,
        "matchup_2_ab_off2_vs_ab_def1": r2,
        "matchup_3_ab_def2_vs_ab_off1": r3,
        "matchup_4_ab_off2_vs_ab_off1": r4,
        "matchup_5_ab_def2_vs_ab_def1": r5,
        "matchup_6_ab_off2_vs_ab_def2": r6,
    }
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nResults saved to experiment_results.json")


if __name__ == '__main__':
    main()