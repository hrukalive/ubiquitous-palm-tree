import random
from copy import deepcopy

from tqdm import tqdm

from games import Game


# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self):  # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",  # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0},  # Initially, white and black have captured 0 pieces.
            'board': grid,  # 8x8 grid representing the board.
        }  # ⚠️ You must use this structure for the state representation.

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
        # Return a dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        moves = []
        board = state["board"]
        player = state["to_move"]
        deltas = [(-1, 0), (-1, -1), (-1, 1)] if player == "WHITE" else [(1, 0), (1, -1), (1, 1)]

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    for dr, dc in deltas:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            target = board[nr][nc]
                            if target == "EMPTY":
                                moves.append({"from": (r, c), "to": (nr, nc)})
                            elif target != player and dc != 0:
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
        obj_copy = deepcopy(state)
        player = state['to_move']
        new_to_move = "BLACK" if player == "WHITE" else "WHITE"
        new_captures = state['captures'].copy()
        new_board = [row[:] for row in state['board']]

        fr_r, fr_c = action["from"]
        to_r, to_c = action["to"]
        piece = new_board[fr_r][fr_c]
        new_board[fr_r][fr_c] = "EMPTY"

        if new_board[to_r][to_c] != "EMPTY":
            new_captures[player] += 1
        new_board[to_r][to_c] = piece

        return {
            'to_move': new_to_move,
            'captures': new_captures,
            'board': new_board
        }

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if not self.terminal_test(state):
            return 0

        board = state['board']
        white_p = sum(row.count("WHITE") for row in board)
        black_p = sum(row.count("BLACK") for row in board)

        white_win = any(board[0][c] == "WHITE" for c in range(8)) or black_p == 0
        black_win = any(board[7][c] == "BLACK" for c in range(8)) or white_p == 0

        if white_win and black_win:
            return 0
        if (player == "WHITE" and white_win) or (player == "BLACK" and black_win):
            return 1
        return -1

    def terminal_test(self, state):
        # #########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state['board']
        white_p = sum(row.count("WHITE") for row in board)
        black_p = sum(row.count("BLACK") for row in board)
        if white_p == 0 or black_p == 0:
            return True
        if any(board[0][c] == "WHITE" for c in range(8)) or any(board[7][c] == "BLACK" for c in range(8)):
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
        print(
            f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    board = state['board']
    own = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)

    return 2 * own + random.random()


def offensive_eval_1(state, player):
    board = state['board']
    opp = "BLACK" if player == "WHITE" else "WHITE"
    opp_p = sum(1 for r in range(8) for c in range(8) if board[r][c] == opp)

    return 2 * (32 - opp_p) + random.random()


def defensive_eval_2(state, player):
    board = state['board']
    own_color = player
    opp_color = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces = 0
    opp_progress = 0
    opp_almost = False

    for r in range(8):
        for c in range(8):
            cell = board[r][c]
            if cell == own_color:
                own_pieces += 1
            elif cell == opp_color:
                if player == "WHITE":
                    opp_progress += r
                    if r == 6:
                        opp_almost = True
                else:
                    opp_progress += (7 - r)
                    if r == 1:
                        opp_almost = True

    val = 5 * own_pieces - 3 * opp_progress
    if opp_almost:
        val -= 100

    return val + random.random()


def offensive_eval_2(state, player):
    board = state['board']
    own_color = player
    opp_color = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces = 0
    my_progress = 0
    my_captures = state['captures'][player]
    my_almost = False

    for r in range(8):
        for c in range(8):
            cell = board[r][c]
            if cell == own_color:
                own_pieces += 1
                if player == "WHITE":
                    my_progress += (7 - r)
                    if r == 1:
                        my_almost = True
                else:
                    my_progress += r
                    if r == 6:
                        my_almost = True

    val = 2 * own_pieces + 4 * my_progress + 8 * my_captures
    if my_almost:
        val += 200

    return val + random.random()


ag_eval_fn = defensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.


##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False):  # ⚠️ DO NOT CHANGE
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
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game,
                                                                                                                state)
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
