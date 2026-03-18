import random
from copy import deepcopy

from numpy.matlib import empty
from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):

    game_count = 0

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
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
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

        board = state['board']
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        actions = []
        direction = -1 if player == "WHITE" else 1

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                position = r + direction

                if not (0 <= position < 8):
                    continue

                if board[position][c] == "EMPTY":
                    actions.append({"from": (r, c), "to": (position, c)})

                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < 8 and board[position][nc] == opponent:
                        actions.append({"from": (r, c), "to": (position, nc)})

        return actions



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
            'to_move': "BLACK" if state['to_move'] == "WHITE" else "WHITE",
            'captures': deepcopy(state['captures']),
            'board': deepcopy(state['board'])
        }

        fx, fy = action["from"]
        tx, ty = action["to"]

        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        if new_state['board'][tx][ty] == opponent:
            new_state['captures'][player] += 1

        new_state["board"][tx][ty] = player
        new_state["board"][fx][fy] = "EMPTY"

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

        board = state["board"]
        white_reached = "WHITE" in board[0]
        black_reached = "BLACK" in board[7]

        white_exists = any(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_exists = any(board[r][c] == "BLACK" for r in range(8) for c in range(8))

        no_moves = (len(self.actions(state)) == 0)

        winner = None
        if white_reached:
            winner = "WHITE"
        elif black_reached:
            winner = "BLACK"
        elif not white_exists:
            winner = "BLACK"
        elif not black_exists:
            winner = "WHITE"
        elif no_moves:
            winner = "BLACK" if state['to_move'] == "WHITE" else "WHITE"

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
        board = state["board"]

        if "WHITE" in board[0]:
            return True
        if "BLACK" in board[7]:
            return True

        white_exists = any(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_exists = any(board[r][c] == "BLACK" for r in range(8) for c in range(8))

        if not white_exists or not black_exists:
            return True

        if len(self.actions(state)) == 0:
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



##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def count_pieces(board):
    w = b = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == "WHITE":
                w += 1
            elif board[r][c] == "BLACK":
                b += 1
    return w, b

def progress_score(board, player):
    score = 0
    if player == "WHITE":
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    score += (7 - r)
    else:
        for r in range(8):
            for c in range(8):
                if board[r][c] == "BLACK":
                    score += r
    return score

def immediate_capture(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    direction = -1 if player == "WHITE" else 1

    caps = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue

            nr = r + direction

            if 0 <= nr < 8:
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < 8 and board[nr][nc] == opponent:
                        caps += 1
    return caps



def defensive_eval_1(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    w, b = count_pieces(board)
    material = (w - b) if player == "WHITE" else (b - w)

    my_progress = progress_score(board, player)
    opp_progress = progress_score(board, opponent)

    opp_caps = immediate_capture(state, opponent)
    my_caps = immediate_capture(state, player)
    
    return 10 * material + 1 * (my_progress - opp_progress) + 2 * my_caps - 3 * opp_caps


def offensive_eval_1(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    w, b = count_pieces(board)
    material = (w - b) if player == "WHITE" else (b - w)

    my_progress = progress_score(board, player)
    my_caps = immediate_capture(state, player)
    opp_caps = immediate_capture(state, opponent)
    
    return 8 * material + 3 * my_progress + 4 * my_caps - 2 * opp_caps


def defensive_eval_2(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    w, b = count_pieces(board)
    material = (w - b) if player == "WHITE" else (b - w)

    my_progress = progress_score(board, player)
    opp_caps = immediate_capture(state, opponent)
    
    return 12 * material + 2 * my_progress - 6 * opp_caps


def offensive_eval_2(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    w, b = count_pieces(board)
    material = (w - b) if player == "WHITE" else (b - w)

    my_progress = progress_score(board, player)
    my_caps = immediate_capture(state, player)

    return 6 * material + 4 * my_progress + 8 * my_caps

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
