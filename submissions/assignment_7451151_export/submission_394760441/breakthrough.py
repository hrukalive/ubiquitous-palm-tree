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
        actions = []

        board = state['board']
        op = "BLACK"
        player = self.to_move(state)
        direction = -1
        if player == "BLACK":
            op = "WHITE"
            direction = 1

        #Looking for every piece of the current player's color
        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    if 8 > r + direction >= 0: #Make sure next row in the players move direction is on the board
                        for m in [-1, 0, 1]: #Checking for valid moves
                            if 8 > c + m >= 0:
                                new_pos = board[r + direction][c + m]
                                if m == 0:
                                    if new_pos == "EMPTY":
                                        actions.append({"from": (r, c), "to": (r + direction, c + m)})
                                else:
                                    if new_pos == "EMPTY" or new_pos == op:
                                        actions.append({"from": (r, c), "to": (r + direction, c + m)})


        return actions

    def result(self, state, action):
        new_state = deepcopy(state)
        board = new_state['board']

        player = "WHITE"
        op = "BLACK"

        if state['to_move'] == "WHITE":
            new_state['to_move'] = "BLACK"
        if state['to_move'] == "BLACK":
            new_state['to_move'] = "WHITE"
            op = "WHITE"
            player = "BLACK"

        from_row, from_col = action['from']
        to_row, to_col = action['to']

        if board[to_row][to_col] == op:
            new_state['captures'][player] += 1

        board[from_row][from_col] = "EMPTY"
        board[to_row][to_col] = player

        new_state['board'] = board

        return new_state

    def utility(self, state, player):
        board = state['board']
        op = "BLACK"
        if player == "BLACK":
            op = "WHITE"

        if state['captures'][player] == 16:
            return 1
        if state['captures'][op] == 16:
            return -1

        for c in range(8):
            if board[0][c] == "WHITE":
                if player == "WHITE":
                    return 1
                return -1
            if board[7][c] == "BLACK":
                if player == "BLACK":
                    return 1
                return -1

        if not self.actions(state):
            return -1

        return 0

    def terminal_test(self, state):
        board = state['board']

        if state['captures']['WHITE'] == 16 or state['captures']['BLACK'] == 16:
            return True

        for c in range(8):
            if board[0][c] == "WHITE" or board[7][c] == "BLACK":
                return True

        if not self.actions(state):
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

# Evaluation functions

def defensive_eval_1(state, player):
    remaining = 16
    if player == "WHITE":
        remaining = 16 - state['captures']['BLACK']
    else:
        remaining = 16 - state['captures']['WHITE']

    return 2 * remaining + random.random()


def offensive_eval_1(state, player):
    op_captured = 16 - state['captures'][player]
    
    return 2 * (32 - op_captured) + random.random()


def defensive_eval_2(state, player):
    remaining = 16
    op = "BLACK"
    board = state['board']
    if player == "WHITE":
        remaining = 16 - state['captures']['BLACK']
    else:
        remaining = 16 - state['captures']['WHITE']

    dist_sum = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == op:
                if player == "WHITE":
                    dist_sum += 7 - c
                else:
                    dist_sum += c

    av_op_dist = dist_sum / (16 - state['captures'][player])
    
    return 2 * remaining + av_op_dist + random.random()


def offensive_eval_2(state, player):
    op_captured = 16 - state['captures'][player]
    board = state['board']
    op = "BLACK"

    if player == "WHITE":
        op = "BLACK"
    else:
        op = "WHITE"

    dist_sum = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    dist_sum += c
                else:
                    dist_sum += 7 - c

    av_dist =  dist_sum / (16 - state['captures'][op])
    return 2 * (32 - op_captured) + (7 - av_dist) + random.random()

ag_eval_fn = defensive_eval_2           # ⚠️ Should be enough to pass AG test, but you may change it.
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
