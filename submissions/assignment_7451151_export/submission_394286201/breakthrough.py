import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to tic-tac-toe example for Breakthrough implementation.

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
        return state["to_move"]

    def actions(self, state):
        moves = []
        board = state["board"]
        player = state["to_move"]

        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    nr = r + direction

                    if 0 <= nr < 8:
                        # Forward
                        if board[nr][c] == "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c)})

                        # Diagonal left
                        if c - 1 >= 0:
                            if board[nr][c - 1] == "EMPTY" or board[nr][c - 1] == opponent:
                                moves.append({"from": (r, c), "to": (nr, c - 1)})

                        # Diagonal right
                        if c + 1 < 8:
                            if board[nr][c + 1] == "EMPTY" or board[nr][c + 1] == opponent:
                                moves.append({"from": (r, c), "to": (nr, c + 1)})

        return moves

    def result(self, state, action):
        new_state = deepcopy(state)
        board = new_state["board"]

        r1, c1 = action["from"]
        r2, c2 = action["to"]

        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Capture check
        if board[r2][c2] == opponent:
            new_state["captures"][player] += 1

        # Move piece
        board[r2][c2] = player
        board[r1][c1] = "EMPTY"

        # Switch player
        new_state["to_move"] = opponent

        return new_state


    def utility(self, state, player):
        board = state["board"]

        white_exists = any("WHITE" in row for row in board)
        black_exists = any("BLACK" in row for row in board)

        white_win = any(board[0][c] == "WHITE" for c in range(8)) or not black_exists
        black_win = any(board[7][c] == "BLACK" for c in range(8)) or not white_exists

        if white_win:
            return 1 if player == "WHITE" else -1
        if black_win:
            return 1 if player == "BLACK" else -1

        return 0


    def terminal_test(self, state):
        board = state["board"]

        # White reaches top
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True

        # Black reaches bottom
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True

        # All pieces captured
        white_exists = any("WHITE" in row for row in board)
        black_exists = any("BLACK" in row for row in board)

        return not white_exists or not black_exists


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



##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    board = state["board"]
    own = sum(row.count(player) for row in board)
    return 2 * own + random.random()


def offensive_eval_1(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_count = sum(row.count(opponent) for row in board)
    return 2 * (32 - opp_count) + random.random()


def defensive_eval_2(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    own = sum(row.count(player) for row in board)
    opp = sum(row.count(opponent) for row in board)

    # Penalize opponent advancement
    advance_penalty = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                advance_penalty += (7 - r) if opponent == "WHITE" else r

    return 3 * own - 0.5 * advance_penalty + random.random()


def offensive_eval_2(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    score = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 5
                score += (7 - r) if player == "WHITE" else r

    opp_count = sum(row.count(opponent) for row in board)
    score += 2 * (16 - opp_count)

    return score + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
