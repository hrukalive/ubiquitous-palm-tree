import random
from copy import deepcopy

from tqdm import tqdm

from games import Game


class Breakthrough(Game):
    def initial_state(self):  # ⚠️ DO NOT CHANGE THIS FUNCTION
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",
            'captures': {"WHITE": 0, "BLACK": 0},
            'board': grid,
        }

    def to_move(self, state):
        return state['to_move']

    def actions(self, state):
        player = state['to_move']
        board = state['board']
        direction = -1 if player == "WHITE" else 1
        legal_moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                new_r = r + direction
                if not (0 <= new_r < 8):
                    continue
                # Straight forward — only if empty
                if board[new_r][c] == "EMPTY":
                    legal_moves.append({"from": (r, c), "to": (new_r, c)})
                # Diagonal forward — allowed if EMPTY or occupied by enemy
                for new_c in [c - 1, c + 1]:
                    if 0 <= new_c < 8 and board[new_r][new_c] != player:
                        legal_moves.append({"from": (r, c), "to": (new_r, new_c)})
        return legal_moves

    def result(self, state, action):
        board = deepcopy(state['board'])
        captures = deepcopy(state['captures'])
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        from_r, from_c = action['from']
        to_r, to_c = action['to']
        if board[to_r][to_c] == opponent:
            captures[player] += 1
        board[to_r][to_c] = board[from_r][from_c]
        board[from_r][from_c] = "EMPTY"
        return {
            'to_move': opponent,
            'captures': captures,
            'board': board,
        }

    def utility(self, state, player):
        board = state['board']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        # Check if player reached enemy home row
        target_row = 0 if player == "WHITE" else 7
        for c in range(8):
            if board[target_row][c] == player:
                return 1
        # Check if opponent reached player's home row
        opp_target = 7 if opponent == "WHITE" else 0
        for c in range(8):
            if board[opp_target][c] == opponent:
                return -1
        # Check all-pieces-captured
        own_count = sum(board[r][c] == player for r in range(8) for c in range(8))
        opp_count = sum(board[r][c] == opponent for r in range(8) for c in range(8))
        if opp_count == 0:
            return 1
        if own_count == 0:
            return -1
        return 0

    def terminal_test(self, state):
        board = state['board']
        # WHITE reaches row 0
        for c in range(8):
            if board[0][c] == "WHITE":
                return True
        # BLACK reaches row 7
        for c in range(8):
            if board[7][c] == "BLACK":
                return True
        # All pieces of either side captured
        white_count = sum(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_count = sum(board[r][c] == "BLACK" for r in range(8) for c in range(8))
        return white_count == 0 or black_count == 0

    def display(self, state):
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print("\n".join("".join(chars[state['board'][r][c]] for c in range(8)) for r in range(8)))
        if self.terminal_test(state):
            if self.to_move(state) == "WHITE":
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {state['to_move']}")
        print(f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")


# ---------------------------------------------------------------------------
# Evaluation functions
# ---------------------------------------------------------------------------

def defensive_eval_1(state, player):
    """Baseline: value = 2 * own_pieces + random()"""
    board = state['board']
    own_pieces = sum(board[r][c] == player for r in range(8) for c in range(8))
    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    """Baseline: value = 2 * (32 - opponent_pieces) + random()"""
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state['board']
    opp_pieces = sum(board[r][c] == opponent for r in range(8) for c in range(8))
    return 2 * (32 - opp_pieces) + random.random()


def defensive_eval_2(state, player):
    """
    Custom defensive evaluation designed to beat Offensive Evaluation 1.

    Features:
    - Base piece count (+2 per own piece)
    - PieceUnderAttack: -8 per own piece threatened by an enemy diagonal
    - PieceConnectHorizontal: +3 per horizontally adjacent same-color pair (forms blocking wall)
    - PieceConnectVertical: +2 per vertically adjacent same-color pair (depth defense)
    - ColumnHole: -4 per column with no own pieces (open lane for enemy)
    - Opponent advancement: -3 per row of enemy advancement toward our home row
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_dir = -1 if opponent == "WHITE" else 1
    score = 0.0

    # Squares attacked by opponent
    attacked = set()
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                nr = r + opp_dir
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        attacked.add((nr, nc))

    own_cols = set()
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_cols.add(c)
                score += 2  # base piece value
                if (r, c) in attacked:
                    score -= 8  # PieceUnderAttack
                # PieceConnectHorizontal
                if c + 1 < 8 and board[r][c + 1] == player:
                    score += 3
                if c - 1 >= 0 and board[r][c - 1] == player:
                    score += 3
                # PieceConnectVertical
                if r + 1 < 8 and board[r + 1][c] == player:
                    score += 2
                if r - 1 >= 0 and board[r - 1][c] == player:
                    score += 2

    # ColumnHole
    for c in range(8):
        if c not in own_cols:
            score -= 4

    # Opponent advancement penalty
    opp_home = 7 if opponent == "WHITE" else 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                adv = opp_home - r if opponent == "WHITE" else r - opp_home
                score -= 3 * adv

    return score + random.random()


def offensive_eval_2(state, player):
    """
    Custom offensive evaluation designed to beat Defensive Evaluation 1.

    Features:
    - PieceDangerValue: +3 per row advanced toward enemy home (rewards forward progress)
    - PieceAlmostWin: +20 per piece on enemy's second-to-last row not under attack
    - PieceUnderAttack: -5 per own piece threatened by enemy diagonal
    - Capture pressure: +4 per opponent piece capturable on the immediate next move
    - Opponent advancement: -2 per row of enemy advancement toward our home
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_dir = -1 if opponent == "WHITE" else 1
    own_dir = -1 if player == "WHITE" else 1
    home_row = 7 if player == "WHITE" else 0
    almost_win_row = 1 if player == "WHITE" else 6
    score = 0.0

    # Squares attacked by opponent
    attacked = set()
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                nr = r + opp_dir
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        attacked.add((nr, nc))

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                # PieceDangerValue: row advancement
                adv = home_row - r if player == "WHITE" else r - home_row
                score += 3 * adv
                # PieceAlmostWin
                if r == almost_win_row and (r, c) not in attacked:
                    score += 20
                # PieceUnderAttack
                if (r, c) in attacked:
                    score -= 5
                # Capture pressure: count capturable enemy pieces from this piece
                nr = r + own_dir
                if 0 <= nr < 8:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and board[nr][nc] == opponent:
                            score += 4

    # Opponent advancement penalty
    opp_home = 7 if opponent == "WHITE" else 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                opp_adv = opp_home - r if opponent == "WHITE" else r - opp_home
                score -= 2 * opp_adv

    return score + random.random()


ag_eval_fn = defensive_eval_1
competition_eval_fn = offensive_eval_2

# ---------------------------------------------------------------------------

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False):  # ⚠️ DO NOT CHANGE
    """Run a round of game with specified agents. Returns the statistic of the gameplay."""
    game = Breakthrough()
    state = game.initial_state()
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game, state)
        state = game.result(state, move)
        if display:
            game.display(state)
        move_count += 1
        if progress:
            pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break
    if progress:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = sum(white_agent.time_per_move) / len(white_agent.time_per_move)
    black_time_per_move = sum(black_agent.time_per_move) / len(black_agent.time_per_move)
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state["captures"]["WHITE"]
    black_captures = state["captures"]["BLACK"]
    if display:
        game.display(state)
    return {
        'winner': 'white' if winner == "WHITE" else 'black' if winner == "BLACK" else None,
        'white_name': white_agent.name,
        'black_name': black_agent.name,
        'total_moves': move_count,
        'white_nodes': white_nodes,
        'black_nodes': black_nodes,
        'white_nodes_per_move': white_nodes_per_move,
        'black_nodes_per_move': black_nodes_per_move,
        'white_time_per_move': white_time_per_move,
        'black_time_per_move': black_time_per_move,
        'white_captures': white_captures,
        'black_captures': black_captures,
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)