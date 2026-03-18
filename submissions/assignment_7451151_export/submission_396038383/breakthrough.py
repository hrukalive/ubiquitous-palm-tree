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
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        player = state["to_move"]
        board = state["board"]

        # WHITE moves up (r-1), BLACK moves down (r+1)
        dr = -1 if player == "WHITE" else 1
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        moves = []

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                nr = r + dr
                if not (0 <= nr < 8):
                    continue

                # Forward move (no capture)
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})

                # Diagonal forward-left
                nc = c - 1
                if 0 <= nc < 8:
                    if board[nr][nc] == "EMPTY" or board[nr][nc] == enemy:
                        moves.append({"from": (r, c), "to": (nr, nc)})

                # Diagonal forward-right
                nc = c + 1
                if 0 <= nc < 8:
                    if board[nr][nc] == "EMPTY" or board[nr][nc] == enemy:
                        moves.append({"from": (r, c), "to": (nr, nc)})

        return moves

    def result(self, state, action):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        new_state = {
            "to_move": state["to_move"],
            "captures": dict(state["captures"]),
            "board": deepcopy(state["board"]),
        }

        player = state["to_move"]
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        fr, fc = action["from"]
        tr, tc = action["to"]

        # Basic sanity (optional): assume action is legal per actions()
        moving_piece = new_state["board"][fr][fc]
        target_piece = new_state["board"][tr][tc]

        # Move piece
        new_state["board"][fr][fc] = "EMPTY"

        # Handle capture (only possible diagonally-forward, but we just check occupant)
        if target_piece == enemy:
            new_state["captures"][player] += 1

        new_state["board"][tr][tc] = moving_piece

        # Alternate turn
        new_state["to_move"] = enemy
        return new_state


    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

        winner = self._winner(state)
        if winner is None:
            return 0
        return 1 if winner == player else -1


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        return self._winner(state) is not None


    # Helper: determine winner

    def _winner(self, state):
        board = state["board"]

        # Win by reaching opponent home row
        if any(board[0][c] == "WHITE" for c in range(8)):
            return "WHITE"
        if any(board[7][c] == "BLACK" for c in range(8)):
            return "BLACK"

        # Win by capturing all opponent pieces
        white_count = 0
        black_count = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_count += 1
                elif board[r][c] == "BLACK":
                    black_count += 1

        if black_count == 0:
            return "WHITE"
        if white_count == 0:
            return "BLACK"

        return None



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
def _count_pieces(board):
    w = b = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == "WHITE":
                w += 1
            elif board[r][c] == "BLACK":
                b += 1
    return w, b

def _progress_score(board, player):
    """
    Measures how far pieces have advanced toward the goal row.
    WHITE wants smaller row indices (toward 0).
    BLACK wants larger row indices (toward 7).
    """
    if player == "WHITE":
        score = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    score += (7 - r)  # more when closer to row 0
        return score
    else:
        score = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "BLACK":
                    score += r  # more when closer to row 7
        return score

def _threatened_pieces(game, state, player):
    """
    Counts how many of player's pieces can be captured immediately by opponent next move.
    """
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    # Create a "same board" state where it's enemy to move, so we can generate enemy capture moves
    tmp = {"to_move": enemy, "captures": state["captures"], "board": state["board"]}
    enemy_moves = game.actions(tmp)

    threatened = 0
    board = state["board"]
    for mv in enemy_moves:
        tr, tc = mv["to"]
        # If enemy moves into a square that currently contains our piece, it's a capture
        if board[tr][tc] == player:
            threatened += 1
    return threatened

def _immediate_capture_moves(game, state, player):
    """
    Counts how many capturing moves player has right now.
    """
    tmp = {"to_move": player, "captures": state["captures"], "board": state["board"]}
    moves = game.actions(tmp)
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    board = state["board"]
    cap = 0
    for mv in moves:
        tr, tc = mv["to"]
        if board[tr][tc] == enemy:
            cap += 1
    return cap
def defensive_eval_1(state, player):

    board = state["board"]
    w, b = _count_pieces(board)
    own = w if player == "WHITE" else b
    return 2 * own + random.random()


def offensive_eval_1(state, player):
    board = state["board"]
    w, b = _count_pieces(board)
    opp = b if player == "WHITE" else w
    return 2 * (32 - opp) + random.random()

def defensive_eval_2(state, player):
    """
       Goal: beat Offensive Eval 1 (which mostly rewards reducing opponent pieces).
       Strategy: punish leaving pieces en prise, punish enemy advancement,
       reward keeping a “wall” and blocking.
       """
    game = Breakthrough()
    winner = game._winner(state)
    if winner is not None:
        return 10_000 if winner == player else -10_000

    board = state["board"]
    w, b = _count_pieces(board)
    own = w if player == "WHITE" else b
    opp = b if player == "WHITE" else w
    enemy = "BLACK" if player == "WHITE" else "WHITE"

    # Defensive features
    threatened = _threatened_pieces(game, state, player)
    enemy_progress = _progress_score(board, enemy)

    # "Homerow defenders" helps stop breakthroughs
    if player == "WHITE":
        home_defenders = sum(1 for c in range(8) if board[7][c] == "WHITE")
    else:
        home_defenders = sum(1 for c in range(8) if board[0][c] == "BLACK")

    mobility = len(game.actions({"to_move": player, "captures": state["captures"], "board": board}))

    val = (
            14 * (own - opp)  # still value material
            - 25 * threatened  # don't hang pieces
            - 4 * enemy_progress  # slow enemy down
            + 6 * home_defenders  # keep a back line
            + 0.3 * mobility
            + random.random()
    )
    return val


def offensive_eval_2(state, player):
    """
       Goal: beat Defensive Eval 1 (which mostly just rewards keeping pieces).
       Strategy: strongly reward (1) win threats, (2) advancement, (3) captures,
       while still caring about material.
       """
    game = Breakthrough()
    winner = game._winner(state)
    if winner is not None:
        return 10_000 if winner == player else -10_000

    board = state["board"]
    w, b = _count_pieces(board)
    own = w if player == "WHITE" else b
    opp = b if player == "WHITE" else w

    progress = _progress_score(board, player) - _progress_score(board, "BLACK" if player == "WHITE" else "WHITE")
    cap_moves = _immediate_capture_moves(game, state, player)

    # Small mobility bonus so agent doesn't freeze
    mobility = len(game.actions({"to_move": player, "captures": state["captures"], "board": board}))

    # Weights tuned to “push forward and trade”
    val = (
            12 * (own - opp)  # material advantage
            + 5 * progress  # advance toward goal
            + 20 * cap_moves  # take captures
            + 0.5 * mobility
            + random.random()
    )
    return val

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
        'final_board': state["board"]
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
