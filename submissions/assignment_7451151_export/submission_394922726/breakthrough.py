import random
from copy import deepcopy

from tqdm import tqdm
import random

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

def opponent(player):
    return "BLACK" if player == "WHITE" else "WHITE"
def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

class Breakthrough(Game):
    @staticmethod
    def opponent(player):
        return opponent(player)

    @staticmethod
    def in_bounds(r, c):
        return in_bounds(r, c)

    WHITE_MOVES = {
        "F": (-1, 0),
        "DR": (-1, 1),
        "DL": (-1, -1),
    }

    BLACK_MOVES = {
        "F": (1, 0),
        "DR": (1, -1),
        "DL": (1, 1),
    }

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
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
        return state["to_move"]

    def actions(self, state):
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]

        board = state["board"]
        player = state["to_move"]
        moveset = self.WHITE_MOVES if player == "WHITE" else self.BLACK_MOVES
        opponent = self.opponent(player)

        legal_actions = []

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                # Tries every possible move
                for move_name, (dr, dc) in moveset.items():
                    nr, nc = r + dr, c + dc
                    if not self.in_bounds(nr, nc):
                        continue

                    target = board[nr][nc]

                    if move_name == "F":
                        if target == "EMPTY":
                            legal_actions.append({"from": (r, c), "to": (nr, nc)})
                    else:
                        if target == "EMPTY" or target == opponent:
                            legal_actions.append({"from": (r, c), "to": (nr, nc)})

        return legal_actions


    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        board = [row[:] for row in state["board"]]
        player = state["to_move"]
        captures = state["captures"].copy()
        opponent = self.opponent(player)

        from_r, from_c = action["from"]
        to_r, to_c = action["to"]

        if board[to_r][to_c] == opponent:
            captures[player] += 1

        board[to_r][to_c] = player
        board[from_r][from_c] = "EMPTY"

        return {
            "to_move": opponent,
            "captures": captures,
            "board": board
        }

    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        # Positive for win, negative for loss, 0 otherwise.

        board = state["board"]
        captures = state["captures"]
        opponent = self.opponent(player)

        # Captured is less than total number of pieces
        if captures[player] >= 16:
            return 1
        if captures[opponent] >= 16:
            return -1

        # Determines whether pieces made it to the other side of the board
        for c in range(8):
            if player == "WHITE":
                if board[0][c] == "WHITE":
                    return 1
                if board[7][c] == "BLACK":
                    return -1
            if player == "BLACK":
                if board[0][c] == "WHITE":
                    return -1
                if board[7][c] == "BLACK":
                    return 1
        return 0

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        if self.utility(state, "WHITE") != 0:
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


def under_attack(state, r, c, player):
    """Determines whether a piece can be captured by opponent"""
    board = state["board"]
    opp = opponent(player)

    if player == "WHITE":
        attackers = [(r - 1, c - 1), (r - 1, c + 1)]
    else:
        attackers = [(r + 1, c - 1), (r + 1, c + 1)]

    for ar, ac in attackers:
        if in_bounds(ar, ac) and board[ar][ac] == opp:
            return True
    return False


def piece_under_attack(state, player):
    """Determine whether piece is under attack"""
    board = state["board"]
    count = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player and under_attack(state, r, c, player):
                count += 1
    return count


def piece_almost_win(state, player):
    """Checks if pieces on enemy’s second farthest row not under attack"""
    board = state["board"]
    target_row = 1 if player == "WHITE" else 6
    count = 0
    for c in range(8):
        if board[target_row][c] == player and not under_attack(state, target_row, c, player):
            count += 1
    return count


def column_hole(state):
    """Checks if column has no pieces"""
    board = state["board"]
    holes = 0
    for c in range(8):
        piece = False
        for r in range(8):
            if board[r][c] != "EMPTY":
                piece = True
                break
        if not piece:
            holes += 1
    return holes

def piece_home_row(state, player):
    """Counts how many pieces are on starting row"""
    board = state["board"]
    home_row = 7 if player == "WHITE" else 0
    count = 0
    for c in range(8):
        if board[home_row][c] == player:
            count += 1
    return count


def piece_danger_value(state, player):
    """Counts how far piece has moved"""
    board = state["board"]
    total = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                total += (7 - r) if player == "WHITE" else r
    return total


def piece_connect_horizontal(state, player):
    """Counts if two pieces that have the same color are next to each other in board horizontally"""
    board = state["board"]
    count = 0
    for r in range(8):
        for c in range(7):
            if board[r][c] == player and board[r][c + 1] == player:
                count += 1
    return count


def piece_connect_vertical(state, player):
    """Counts if two pieces that have the same color are next to each other in board vertically"""
    board = state["board"]
    count = 0
    for r in range(7):
        for c in range(8):
            if board[r][c] == player and board[r + 1][c] == player:
                count += 1
    return count


def piece_count(state, player):
    """Counts how many pieces the player has remaining"""
    board = state["board"]
    count = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                count += 1
    return count

def pieces_in_half(state, player, enemy=False):
    """Counts pieces in either player's half or opponent's half"""
    board = state["board"]
    count = 0

    if player == "WHITE":
        start_r, end_r = (0, 4) if enemy else (4, 8)
    else:
        start_r, end_r = (4, 8) if enemy else (0, 4)

    for r in range(start_r, end_r):
        for c in range(8):
            if board[r][c] == player:
                count += 1

    return count


def defensive_eval_1(state, player):
    opp = opponent(player)

    capture = state["captures"][player] - state["captures"][opp]
    attacked_diff = piece_under_attack(state, opp) - piece_under_attack(state, player)
    almost_diff = piece_almost_win(state, opp) - piece_almost_win(state, player)
    home = piece_home_row(state, player) - piece_home_row(state, opp)

    return (
        6 * attacked_diff +
        4 * almost_diff +
        2 * capture +
        1 * home
    )


def offensive_eval_1(state, player):
    opp = opponent(player)

    capture = state["captures"][player] - state["captures"][opp]
    danger = piece_danger_value(state, player) - piece_danger_value(state, opp)
    almost_diff = piece_almost_win(state, player) - piece_almost_win(state, opp)
    attacked_diff = piece_under_attack(state, opp) - piece_under_attack(state, player)

    return (
        4 * danger +
        4 * almost_diff +
        2 * capture +
        2 * attacked_diff
    )


def defensive_eval_2(state, player):
    opp = opponent(player)

    capture = state["captures"][player] - state["captures"][opp]
    pieces = piece_count(state, player) - piece_count(state, opp)

    attacked_diff = piece_under_attack(state, opp) - piece_under_attack(state, player)

    # Keep pieces grouped
    conn = (piece_connect_horizontal(state, player) + piece_connect_vertical(state, player)) - \
           (piece_connect_horizontal(state, opp) + piece_connect_vertical(state, opp))

    opp_in_my_half = pieces_in_half(state, opp, False)
    almost_diff = piece_almost_win(state, player) - piece_almost_win(state, opp)

    holes = column_hole(state)
    home = piece_home_row(state, player) - piece_home_row(state, opp)

    return (
        5 * attacked_diff +
        4 * pieces +
        2 * capture +
        2 * conn +
        3 * almost_diff -
        3 * opp_in_my_half -
        2 * holes +
        1 * home
    )


def offensive_eval_2(state, player):
    opp = opponent(player)

    capture = state["captures"][player] - state["captures"][opp]
    danger = piece_danger_value(state, player) - piece_danger_value(state, opp)
    almost_diff = piece_almost_win(state, player) - piece_almost_win(state, opp)
    attacked_diff = piece_under_attack(state, opp) - piece_under_attack(state, player)

    # Encourage pieces across halfway point of board
    enemy_half = pieces_in_half(state, player, True) - pieces_in_half(state, opp, True)

    return (
        6 * danger +
        6 * almost_diff +
        2 * capture +
        2 * attacked_diff +
        2 * enemy_half
    )


ag_eval_fn = defensive_eval_2
competition_eval_fn = defensive_eval_2

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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
