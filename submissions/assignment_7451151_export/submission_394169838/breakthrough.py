import random
import math
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
        current_action = state['to_move']
        direction = None
        if current_action == 'WHITE':
            direction = -1
        else:
            direction = 1
        moves = []
        board = state['board']
        for row in range(len(board)):
            for col in range(len(board[0])):
                next_row = row+direction
                if board[row][col] == current_action and 0 <= next_row < len(board):
                    fr = (row,col)

                    #checks front
                    if board[row+direction][col] == "EMPTY":
                        to = (next_row, col)
                        moves.append({"from": fr, "to": to})
                    
                    #checks diagonals
                    for next_col in (col - 1, col + 1):
                        if 0 <= next_col < len(board[0]) and board[next_row][next_col] != current_action:
                            to = (next_row, next_col)
                            moves.append({"from": fr, "to": to})
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

        captures = dict(state['captures'])
        board = [row[:] for row in state['board']]

        fr = action['from']
        to = action['to']
        board[fr[0]][fr[1]] = 'EMPTY'
        if board[to[0]][to[1]] != 'EMPTY':
            captures[state['to_move']] += 1
        board[to[0]][to[1]] = state['to_move']
        
        return {
            'to_move': 'BLACK' if state['to_move'] == 'WHITE' else 'WHITE',
            'captures': captures,
            'board': board
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
        white_count = 0
        black_count = 0
        board = state['board']

        for row in range(len(board)):
            for col in range(len(board[0])):
                cell = board[row][col] 
                if cell == 'WHITE':
                    white_count += 1
                elif cell == 'BLACK':
                    black_count += 1
        
        if white_count == 0:
            return 100000000000 if player == 'BLACK' else -100000000000
        if black_count == 0:
            return 100000000000 if player == 'WHITE' else -100000000000

        
        for col in range(len(board[0])):
            if board[0][col] == 'WHITE':
                return 100000000000 if player == 'WHITE' else -100000000000
            if board[len(board)-1][col] == 'BLACK':
                return 100000000000 if player == 'BLACK' else -100000000000
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        if not self.actions(state):
            return True
        board = state['board']
        for col in range(len(board[0])):
            if board[0][col] == 'WHITE' or board[len(board)-1][col] == 'BLACK':
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
    captures = state['captures']
    if player == 'WHITE':
        score = 16 - captures['BLACK']
        return score + random.random()
    else:
        score = 16 - captures['WHITE']
        return score + random.random()
    return ...


def offensive_eval_1(state, player):
    captures = state['captures']
    if player == 'WHITE':
        score = captures['WHITE']
        return score + random.random()
    else:
        score = captures['BLACK']
        return score + random.random()
    return ...


def defensive_eval_2(state, player):
    board = state['board']
    center_count = 0
    under_attack = 0
    defended = 0
    if player == 'WHITE':
        direction = -1
    else:
        direction = 1
    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = board[row][col]
            next_row = row+direction
            prev_row = row - direction
            if cell == "EMPTY":
                continue

            #check under attack and defended

            if cell == player:
                for next_col in (col - 1, col + 1):
                    if 0 <= next_col < len(board[0]):
                        if 0 <= next_row < len(board):
                            c = board[next_row][next_col]
                            if c != player and c != "EMPTY":
                                under_attack += 1
                        if 0 <= prev_row < len(board):
                            c = board[prev_row][next_col]
                            if c == player:
                                defended += 1

            #center pieces
            if 2 <= row <= 5 and 2 <= col <= 5:
                if cell == player:
                    center_count += 1
                else:
                    center_count -= 1

    return 1 * defended + 1 * center_count - 1 * under_attack + random.random()

def offensive_eval_2(state, player):
    board = state['board']

    center_count = 0
    farthest_piece_w = 0
    farthest_piece_b = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = board[row][col]

            if cell == "EMPTY":
                continue
            
            #farthest piece
            if cell == "WHITE":
                dist = 8 - row
                if dist > farthest_piece_w:
                    farthest_piece_w = dist
            else:
                if row > farthest_piece_b:
                    farthest_piece_b = row

            #center pieces
            if 2 <= row <= 5 and 2 <= col <= 5:
                if cell == player:
                    center_count += 1
                else:
                    center_count -= 1
    
    if player == "WHITE":
        farthest_dif = farthest_piece_w - farthest_piece_b
    else:
        farthest_dif = farthest_piece_b - farthest_piece_w

    return farthest_dif * 4 + center_count + random.random()


ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
        'state': state
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
