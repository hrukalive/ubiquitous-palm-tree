import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self): # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",                   # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0}, # Initially, white and black have captured 0 pieces.
            'board': grid,                        # 8x8 grid representing the board.
        } # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):
        return state['to_move']

    def actions(self, state):
        board = state['board']
        player = state['to_move']
        moves = []

        # WHITE moves up (decreasing row), BLACK moves down (increasing row)
        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                nr = r + direction

                if not (0 <= nr < 8):
                    continue

                # Forward move (only if empty)
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})

                # Diagonal captures (can capture opponent, cannot move to own piece)
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < 8 and board[nr][nc] != player:
                        # Can move diagonally if empty or opponent
                        moves.append({"from": (r, c), "to": (nr, nc)})

        return moves

    def result(self, state, action):
        board = deepcopy(state['board'])
        captures = dict(state['captures'])
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        fr, fc = action['from']
        tr, tc = action['to']

        if board[tr][tc] == opponent:
            captures[player] += 1

        board[tr][tc] = player
        board[fr][fc] = "EMPTY"

        return {
            'to_move': opponent,
            'captures': captures,
            'board': board,
        }


    def utility(self, state, player):
        # Called on terminal states
        # The player who just moved wins (the one who is NOT to_move)
        winner = "BLACK" if state['to_move'] == "WHITE" else "WHITE"
        if winner == player:
            return 1
        else:
            return -1


    def terminal_test(self, state):
        board = state['board']

        # Check if WHITE reached row 0
        for c in range(8):
            if board[0][c] == "WHITE":
                return True

        # Check if BLACK reached row 7
        for c in range(8):
            if board[7][c] == "BLACK":
                return True

        # Check if all pieces of one player are captured
        white_count = sum(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_count = sum(board[r][c] == "BLACK" for r in range(8) for c in range(8))

        if white_count == 0 or black_count == 0:
            return True

        return False


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



def _count_pieces(state, player):
    board = state['board']
    return sum(board[r][c] == player for r in range(8) for c in range(8))

def _advancement(state, player):
    """Sum of how far advanced each piece is (toward opponent's side)."""
    board = state['board']
    total = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    total += (7 - r)  # closer to row 0 = more advanced
                else:
                    total += r        # closer to row 7 = more advanced
    return total

def defensive_heuristic_1(state, player):
    """More pieces remaining = better. Baseline defensive eval."""
    own = _count_pieces(state, player)
    return 2 * own + random.random()


def offensive_heuristic_1(state, player):
    """Fewer opponent pieces = better. Baseline offensive eval."""
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_pieces = _count_pieces(state, opponent)
    return 2 * (32 - opp_pieces) + random.random()


def defensive_heuristic_2(state, player):
    """
    Defensive: prioritize keeping pieces alive and staying in defensive formation.
    - Reward having more pieces
    - Penalize opponent advancement
    - Small reward for own advancement (not primary focus)
    """
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces = _count_pieces(state, player)
    opp_pieces = _count_pieces(state, opponent)

    own_adv = _advancement(state, player)
    opp_adv = _advancement(state, opponent)

    score = (
        3.0 * own_pieces          # keep own pieces
        - 2.0 * opp_pieces        # opponent having pieces is bad
        + 0.5 * own_adv           # slight advancement bonus
        - 1.5 * opp_adv           # penalize opponent advancement heavily
        + random.random() * 0.1
    )
    return score


def offensive_heuristic_2(state, player):
    """
    Offensive: prioritize advancing pieces and capturing opponent pieces.
    - Reward own advancement strongly
    - Reward capturing opponent pieces
    - Less concern about own piece count
    """
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces = _count_pieces(state, player)
    opp_pieces = _count_pieces(state, opponent)

    own_adv = _advancement(state, player)

    score = (
        2.0 * own_adv             # strongly reward advancement
        - 3.0 * opp_pieces        # capturing opponents is very good
        + 1.0 * own_pieces        # having pieces is good
        + random.random() * 0.1
    )
    return score

defensive_eval_2 = defensive_heuristic_2
offensive_eval_2 = offensive_heuristic_2

ag_eval_fn = defensive_heuristic_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_heuristic_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.

    :param white_agent: An agent that plays white.
    :param black_agent: An agent that plays black.
    :param max_moves: The maximum number of moves to play.
    :param display: Whether to display the game state during play.
    :param progress: Whether to show a progress bar.
    :return: The statistic of the game play.
    """
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
    white_time_per_move = (sum(white_agent.time_per_move) / len(white_agent.time_per_move))
    black_time_per_move = (sum(black_agent.time_per_move) / len(black_agent.time_per_move))
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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_heuristic_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_heuristic_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
