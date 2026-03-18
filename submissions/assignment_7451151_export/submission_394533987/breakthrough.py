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
        moves = []
        player = state['to_move']
        board = state['board']
        direction = -1 if player == "WHITE" else 1
        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                nr = r + direction
                if nr < 0 or nr > 7:
                    continue
                # Forward: only if empty (no captures straight ahead)
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})
                # Diagonal left and right: empty or opponent (capture)
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < 8 and board[nr][nc] != player:
                        moves.append({"from": (r, c), "to": (nr, nc)})
        return moves

    def result(self, state, action):
        new_state = deepcopy(state)
        fr, fc = action["from"]
        tr, tc = action["to"]
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        if new_state['board'][tr][tc] == opponent:
            new_state['captures'][player] += 1
        new_state['board'][tr][tc] = player
        new_state['board'][fr][fc] = "EMPTY"
        new_state['to_move'] = opponent
        return new_state


    def utility(self, state, player):
        if not self.terminal_test(state):
            return 0
        winner = "BLACK" if state['to_move'] == "WHITE" else "WHITE"
        return 1 if player == winner else -1


    def terminal_test(self, state):
        board = state['board']
        # WHITE reached BLACK's home row (row 0)
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True
        # BLACK reached WHITE's home row (row 7)
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True
        # All pieces of one color captured
        white_exists = any(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        if not white_exists:
            return True
        black_exists = any(board[r][c] == "BLACK" for r in range(8) for c in range(8))
        if not black_exists:
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
    board = state['board']
    own_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)
    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opponent_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent)
    return 2 * (32 - opponent_pieces) + random.random()


def defensive_eval_2(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces = 0
    connections = 0
    under_attack = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue
            own_pieces += 1
            # Horizontal connection with neighbor to the right
            if c + 1 < 8 and board[r][c + 1] == player:
                connections += 1
            # Check if under attack from opponent diagonal
            if player == "WHITE":
                attackers = [(r - 1, c - 1), (r - 1, c + 1)]
            else:
                attackers = [(r + 1, c - 1), (r + 1, c + 1)]
            for ar, ac in attackers:
                if 0 <= ar < 8 and 0 <= ac < 8 and board[ar][ac] == opponent:
                    under_attack += 1
                    break
    return (2 * own_pieces
            + 0.5 * connections
            - 1.0 * under_attack
            + random.random())


def offensive_eval_2(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opponent_pieces = 0
    advancement = 0
    almost_winning = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    advancement += (7 - r)
                    if r == 1:
                        almost_winning += 1
                else:
                    advancement += r
                    if r == 6:
                        almost_winning += 1
            elif board[r][c] == opponent:
                opponent_pieces += 1
    return (2 * (32 - opponent_pieces)
            + 0.5 * advancement
            + 5 * almost_winning
            + random.random())

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
