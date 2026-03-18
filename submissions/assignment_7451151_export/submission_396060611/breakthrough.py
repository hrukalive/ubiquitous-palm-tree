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
        return state["to_move"]

    def actions(self, state):
        board = state["board"]
        player = state["to_move"]
        moves = []

        direction = -1 if player == "WHITE" else 1

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                nr = r + direction
                if not (0 <= nr < 8):
                    continue

                # forward: must be empty
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})

                # diagonal left: can move if not own piece
                if c - 1 >= 0 and board[nr][c - 1] != player:
                    moves.append({"from": (r, c), "to": (nr, c - 1)})

                # diagonal right: can move if not own piece
                if c + 1 < 8 and board[nr][c + 1] != player:
                    moves.append({"from": (r, c), "to": (nr, c + 1)})

        return moves

    def result(self, state, action):
        new_state = deepcopy(state)
        board = new_state["board"]
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        r1, c1 = action["from"]
        r2, c2 = action["to"]

        if board[r2][c2] == opponent:
            new_state["captures"][player] += 1

        board[r2][c2] = player
        board[r1][c1] = "EMPTY"
        new_state["to_move"] = opponent

        return new_state

    def utility(self, state, player):

        if not self.terminal_test(state):
            return 0

        winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"

        if winner == player:
            return 1
        else:
            return -1

    def terminal_test(self, state):
        board = state["board"]

        for c in range(8):
            if board[0][c] == "WHITE":
                return True
            if board[7][c] == "BLACK":
                return True

        white_count = 0
        black_count = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_count += 1
                elif board[r][c] == "BLACK":
                    black_count += 1

        if white_count == 0 or black_count == 0:
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

def defensive_eval_1(state, player):

    board = state["board"]

    own = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own += 1

    return 2 * own + random.random()

def offensive_eval_1(state, player):

    board = state["board"]

    opponent = "BLACK" if player == "WHITE" else "WHITE"

    opp = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                opp += 1

    return 2 * (32 - opp) + random.random()


def offensive_eval_2(state, player):

    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    score = 0

    for r in range(8):
        for c in range(8):

            if board[r][c] == player:

                if player == "WHITE":
                    score += (7 - r)

                else:
                    score += r

            if board[r][c] == opponent:
                score -= 1

    return score + random.random()


def defensive_eval_2(state, player):

    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    own = 0
    opp = 0

    for r in range(8):
        for c in range(8):

            if board[r][c] == player:
                own += 1

            if board[r][c] == opponent:
                opp += 1

    return 3 * own - opp + random.random()

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
