import json

from breakthrough import offensive_eval_1, defensive_eval_1, Breakthrough
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
# YOUR NAME: Brandon Small
# YOUR WPI ID: 901015254
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided heuristics, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


# Perform the necessary experiments here to generate data required by the report.

def board_to_str(board):
    """Return a labelled ASCII grid of the board"""
    chars = {'WHITE': 'W', "BLACK": "B", "EMPTY": "."}
    lines = ['      ' + '  '.join(str(c) for c in range(8)),
             '      ' + '-' * 23]
    for r in range(8):
        row = '  '.join(chars[board[r][c]] for c in range(8))
        lines.append(f'  {r} | {row}')
    return '\n'.join(lines)


def replay_for_final_board(white_player, black_player, max_moves=400):
    game = Breakthrough()
    state = game.initial_state()
    white_player.reset()
    black_player.reset()
    move_count = 0
    while True:
        if state['to_move'] == 'WHITE':
            move = white_player.select_move(game, state)
        else:
            move = black_player.select_move(game, state)
        state = game.result(state, move)
        move_count += 1
        if game.terminal_test(state) or move_count >= max_moves:
            break
    return state

def print_game_report(result, final_state):
    """Print everything need for the reported for completed games"""
    winner_str = result['winner'].upper() if result['winner'] else 'DRAW (max moves reached)'

    # Final board state and winner
    print(f"\n Winner: {winner_str}")
    print(f"  Final board (W=White, B=Black, .=Empty):")
    for line in board_to_str(final_state['board']).splitlines():
        print(f"        {line}")

    # Captures and total moves
    print(f"\n  Captures and game length:")
    print(f"  White captured : {result['white_captures']} opponent workers")
    print(f"  Black captured : {result['black_captures']} opponent workers")
    print(f"  Total moves: {result['total_moves']}")


def run_matchup(white_player, black_player, num_games=5, max_moves=400):
    """Run multiple games for a matchup and collect the results"""
    results = []
    white_wins = 0
    black_wins = 0
    draws = 0

    for i in range(num_games):
        white_player.reset()
        black_player.reset()
        result = play_game(white_player, black_player, max_moves=max_moves, display=False, progress=False)
        results.append(result)
        if result['winner'] == 'white':
            white_wins += 1
        elif result['winner'] == 'black':
            black_wins += 1
        else:
            draws += 1
        print(f" Game {i+1}/{num_games}: Winner: {result['winner']}, "
               f"Moves={result['total_moves']}, "
               f"W-nodes/move={result['white_nodes_per_move']:.1f}, "
               f"B-nodes/move={result['black_nodes_per_move']:.1f}")

    avg_white_nodes = sum(r['white_nodes_per_move'] for r in results) / num_games
    avg_black_nodes = sum(r['black_nodes_per_move'] for r in results) / num_games
    avg_white_time = sum(r['white_time_per_move'] for r in results) / num_games
    avg_black_time = sum(r['black_time_per_move'] for r in results) / num_games
    avg_moves = sum(r['total_moves'] for r in results) / num_games

    summary = {
        'white_name': white_player.name,
        'black_name': black_player.name,
        'num_games': num_games,
        'white_wins': white_wins,
        'black_wins': black_wins,
        'draws': draws,
        'avg_total_moves': avg_moves,
        'avg_white_nodes_per_move': avg_white_nodes,
        'avg_black_nodes_per_move': avg_black_nodes,
        'avg_white_time_per_move': avg_white_time,
        'avg_black_time_per_move': avg_black_time,
    }

    # Replay to get the final board state
    final_state = replay_for_final_board(white_player, black_player, max_moves)
    print_game_report(result, final_state)

    return summary


def main():
    NUM_GAMES = 5 # Number of games per matchup

    print("=" * 70)
    print("GAME EXPERIMENTS")
    print("=" * 70)

    all_results = {}

    # MATCHUP 1: Minimax (Offensive Eval 1) vs AlphaBeta (Offensive Eval 1)
    print("\n[Matchup 1] Minimax (0ff1) [WHITE] vs AlphaBeta (Off1) [BLACK]")
    white = MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 1'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")


    # MATCHUP 2: Minimax (Offensive Eval 1) vs AlphaBeta (Defensive Eval 1)
    print("\n[Matchup 2] AlphaBeta (0ff2) [WHITE] vs AlphaBeta (Def1) [BLACK]")
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 2'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")


    # MATCHUP 3: AlphaBeta (Defensive Eval 1) vs AlphaBeta (Offensive Eval 1)
    print("\n[Matchup 3] AlphaBeta (Def2) [WHITE] vs AlphaBeta (Off1) [BLACK]")
    white = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 3'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")


    # MATCHUP 4: AlphaBeta (Offensive Eval 2) vs AlphaBeta (Offensive Eval 1)
    print("\n[Matchup 4] AlphaBeta (0ff2) [WHITE] vs AlphaBeta (Off1) [BLACK]")
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 4'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")


    # MATCHUP 5: AlphaBeta (Offensive Eval 1) vs AlphaBeta (Offensive Eval 1)
    print("\n[Matchup 5] AlphaBeta (Def2) [WHITE] vs AlphaBeta (Def1) [BLACK]")
    white = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 5'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")

    # MATCHUP 6: AlphaBeta (Offensive Eval 1) vs AlphaBeta (Offensive Eval 1)
    print("\n[Matchup 6] AlphaBeta (0ff2) [WHITE] vs AlphaBeta (Def2) [BLACK]")
    white = AlphaBetaAgent("AlphaBeta Off2", depth=4, eval_fn=offensive_eval_2)
    black = AlphaBetaAgent("AlphaBeta Def2", depth=4, eval_fn=defensive_eval_2)
    summary = run_matchup(white, black, num_games=NUM_GAMES)
    all_results['matchup 6'] = summary
    print(f" -> White wins: {summary['white_wins']}, Black wins: {summary['black_wins']}, "
          f"Draws: {summary['draws']}")
    print(f" -> Avg moves: {summary['avg_total_moves']:.1f}, "
          f"W nodes/move: {summary['avg_white_nodes_per_move']:.1f}, "
          f"B nodes/move: {summary['avg_black_nodes_per_move']:.1f}")


    # Save results to JSON
    with open("experiment_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\n\nAll results saved to experiment_results.json")

    # Print the final summary
    print("\n" + "=" * 90)
    print(f"{'Matchup':<10} {'White Player':<22} {'Black Player':<22} {'W':<4} {'B':<4} {'D':<4}")
    print("-" * 88)
    for key, r in all_results.items():
        print(f"{key:<10} {r['white_name']:<22} {r['black_name']:<22} "
              f"{r['white_wins']:<4} {r['black_wins']:<4} {r['draws']:<4}")
    print("-" * 90)

if __name__ == '__main__':
    main()
