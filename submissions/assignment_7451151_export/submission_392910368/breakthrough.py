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
        board = state['board']
        player = state['to_move']
        moves_array = []

        # Loop over all positions on the board to see if there is a piece on it
        for r in range(0, 8):
            for c in range(0, 8):
                # If you find a piece, check its color
                if board[r][c] != 'EMPTY':
                    available_moves = []
                    # If its a black
                    if player == 'BLACK':
                        if board[r][c] == 'BLACK':
                            # If there is an empty space in front of it, add it to the list of available moves
                            if board[r + 1][c] == 'EMPTY':
                                available_moves.append((r + 1, c))

                            # Check if the piece can move left diagonally
                            if c != 0:
                                if board[r + 1][c - 1] != 'BLACK':
                                    available_moves.append((r + 1, c - 1))
                            
                            # Check if the piece can move right diagonally
                            if c != 7:
                                if board[r + 1][c + 1] != 'BLACK':
                                    available_moves.append((r + 1, c + 1))
                    else:
                        # If its a white
                        if board[r][c] == 'WHITE':
                            # If there is an empty space in front of it, add it to the list of available moves
                            if board[r - 1][c] == 'EMPTY':
                                available_moves.append((r - 1, c))

                            # Check if the piece can move left diagonally
                            if c != 0:
                                if board[r - 1][c - 1] != 'WHITE':
                                    available_moves.append((r - 1, c - 1))
                            
                            # Check if the piece can move right diagonally
                            if c != 7:
                                if board[r - 1][c + 1] != 'WHITE':
                                    available_moves.append((r - 1, c + 1))

                    for move in available_moves:
                        moves_array.append({'from': (r, c), 'to': move})

        return moves_array

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
        state_copy = deepcopy(state)
        piece_from = action['from']
        piece_to = action['to']

        state_copy['board'][piece_from[0]][piece_from[1]] = 'EMPTY'
        if state_copy['to_move'] == 'BLACK':
            if state_copy['board'][piece_to[0]][piece_to[1]] == 'WHITE':
                state_copy['captures']['BLACK'] += 1
            state_copy['board'][piece_to[0]][piece_to[1]] = 'BLACK'
            state_copy['to_move'] = 'WHITE'

        else:
            if state_copy['board'][piece_to[0]][piece_to[1]] == 'BLACK':
                state_copy['captures']['WHITE'] += 1
            state_copy['board'][piece_to[0]][piece_to[1]] = 'WHITE'
            state_copy['to_move'] = 'BLACK'
        
        return state_copy

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if player == 'WHITE':
            for i in range(0, 8):
                if state['board'][0][i] == 'WHITE':
                    return 1
                if state['board'][7][i] == 'BLACK':
                    return -1
        else:
            for i in range(0, 8):
                if state['board'][7][i] == 'BLACK':
                    return 1
                if state['board'][0][i] == 'WHITE':
                    return -1
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        white_piece_count = 0
        black_piece_count = 0        
        for i in range(0, 8):
            if state['board'][0][i] == 'WHITE' or state['board'][7][i] == 'BLACK':
                return True
            for j in range(0, 8):
                if state['board'][i][j] == 'WHITE':
                    white_piece_count += 1
                if state['board'][i][j] == 'BLACK':
                    black_piece_count += 1
        if white_piece_count == 0 or black_piece_count == 0:
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
    return 2 * (state['captures'][player]) + random.random()


def offensive_eval_1(state, player):
    opponent = 'BLACK' if player == 'WHITE' else 'WHITE'
    return 2 * (state['captures'][opponent]) + random.random()


def defensive_eval_2(state, player):
    black_levels = {0: 4, 1: 3, 2: 2, 3: 1}
    white_levels = {7: 4, 6: 3, 5: 2, 4: 1}
    evaluation = 0
    board = state['board']
    
    occupied_lanes = set()

    # Add to score for the more pieces the player still has on the board
    evaluation += 16 - state['captures']['WHITE' if player == 'BLACK' else 'BLACK']

    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                # Add to score if the agent is playing back
                if player == "BLACK":
                    evaluation += black_levels.get(i, 0)
                    # Add to the score if the agent is creating diagonal structures
                    if i > 0 and 1 <= j <= 6:
                        if board[i-1][j+1] == 'BLACK' or board[i-1][j-1] == 'BLACK':
                            evaluation += 3
                else:
                    evaluation += white_levels.get(i, 0)
                    if i < 7 and 1 <= j <= 6:
                        if board[i+1][j+1] == 'WHITE' or board[i+1][j-1] == 'WHITE':
                            evaluation += 3
                # Add to the score if the agent is keeping all columns of the board occupied
                occupied_lanes.add(j)

    evaluation += len(occupied_lanes)

    return evaluation

def offensive_eval_2(state, player):
    white_levels = {0: 1000, 1: 3, 2: 2, 3: 1}
    black_levels = {7: 1000, 6: 3, 5: 2, 4: 1}
    evaluation = 0
    board = state['board']
    
    # Add score for capturing
    opponent = 'BLACK' if player == 'WHITE' else 'WHITE'
    evaluation += state['captures'][opponent]

    # Add score how far up the agent is playing
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                # Add position score
                if player == "BLACK":
                    evaluation += black_levels.get(i, 0)
                    # Diagonal check for Black
                    if i < 7 and 1 <= j <= 6:
                        if board[i+1][j+1] == 'BLACK' or board[i+1][j-1] == 'BLACK':
                            evaluation += 3
                else:
                    evaluation += white_levels.get(i, 0)
                    # Diagonal check for White
                    if i > 0 and 1 <= j <= 6:
                        if board[i-1][j+1] == 'WHITE' or board[i-1][j-1] == 'WHITE':
                            evaluation += 3

    return evaluation

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
