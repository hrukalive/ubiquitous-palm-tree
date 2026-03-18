import random
from copy import deepcopy
from operator import truediv
from token import LEFTSHIFT

from numpy.f2py.auxfuncs import isfunction_wrap
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
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

        return state['to_move']

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

        # Local Variables
        active = state['to_move']   # Active Team (can make a move)
        remaining = 16              # Number of remaining active pieces
        pieceLocations = []                  # List of remaining active piece locations
        states = []

        # Calculate 'remaining'
        if state['to_move'] == "WHITE": remaining = 16 - state['captures']['BLACK']
        if state['to_move'] == "BLACK": remaining = 16 - state['captures']['WHITE']

        # Loop through current board looking for pieces that could move and add their locations to 'Valid'
        for r_idx, row in enumerate(state['board']):

            if remaining == 0: break
            for c_idx, col in enumerate(row):

                if col == active:

                    pieceLocations.append((r_idx, c_idx))
                    remaining -= 1
                    if remaining == 0: break

        for piece in pieceLocations:
            states.extend(self.legal_moves(state, piece))

        return states

    def legal_moves(self, state, pawn):

        # Projected Tiles
        forward = (0, 0)
        diagL = (0, 0)
        diagR = (0, 0)
        states = []

        # Pawn must move "Up" the board
        if state['to_move'] == "WHITE":

            # Project 3 Possible Moves
            forward = ((pawn[0] - 1), pawn[1], )
            diagL = ((pawn[0] - 1), (pawn[1] - 1))
            diagR = ((pawn[0] - 1), (pawn[1] + 1))

        # Pawn must move "Down" the board
        else:

            # Project 3 Possible Moves
            forward = ((pawn[0] + 1), pawn[1], )
            diagL = ((pawn[0] + 1), pawn[1] - 1)
            diagR = ((pawn[0] + 1), pawn[1] + 1)

        # Validate Projected Moves

        if 0 <= forward[0] <= 7 and 0 <= forward[1] <= 7:

            if  0 <= diagL[1] <= 7:

                if state['board'][diagL[0]][diagL[1]] != state['to_move']:
                    aValidMove = {
                        "from": pawn,
                        "to": diagL
                    }
                    states.append(aValidMove)

            if 0 <= diagR[1] <= 7:

                if state['board'][diagR[0]][diagR[1]] != state['to_move']:
                    aValidMove = {
                        "from": pawn,
                        "to": diagR
                    }
                    states.append(aValidMove)

            if state['board'][forward[0]][forward[1]] == "EMPTY":
                aValidMove = {
                    "from": pawn,
                    "to": forward
                }
                states.append(aValidMove)

        # Return Final Updated List Of Legal Moves (Possible States)
        return states


    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).

        # Clone the State
        stateClone = deepcopy(state)

        # Grab Pawn
        pawn = stateClone['board'][action['from'][0]][action['from'][1]]

        # Set 'From' tile to 'EMPTY'
        stateClone['board'][action['from'][0]][action['from'][1]] = 'EMPTY'

        # Set 'To' tile to pawn
        end = stateClone['board'][action['to'][0]][action['to'][1]]
        if end != 'EMPTY':
            if pawn == 'WHITE':

                stateClone['captures']["WHITE"] += 1

            if pawn == 'BLACK':

                stateClone['captures']['BLACK'] += 1

        stateClone['board'][action['to'][0]][action['to'][1]] = pawn

        if stateClone['to_move'] == "WHITE": stateClone['to_move'] = "BLACK"
        else: stateClone['to_move'] = "WHITE"

        # Return Updated State
        return stateClone


    def utility(self, state, player):

        # Return the value to the perspective of the "player";
        # Positive for win, negative for loss, 0 otherwise.

        result = 0
        isActive = False # if we know there is a winner, is the winner the active "player"?

        if not self.terminal_test(state): return result

        else:
            if state['captures']['WHITE'] == 16 and player == 'WHITE':
                    isActive = True

            if state['captures']['BLACK'] == 16 and player == 'BLACK':
                    isActive = True

            for c_idx, col in enumerate(state['board'][0]):

                if col == 'WHITE' and player == 'WHITE':
                    isActive = True

            for c_idx, col in enumerate(state['board'][7]):

                if col == "BLACK" and player == 'BLACK':
                    isActive = True

            if isActive: result = 1

            else: result = -1

        return result


    def terminal_test(self, state):

        # Return True if this is a terminal state, False otherwise.
        if state['captures']['WHITE'] == 16: return True
        elif state['captures']['BLACK'] == 16: return True

        else:

            for c_idx, col in enumerate(state['board'][0]):
                if col == 'WHITE': return True

            for c_idx, col in enumerate(state['board'][7]):
                if col == 'BLACK': return True

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
    
    #  2 * ( number_of_own_pieces_remaining ) + random() .
    finalResult = 0

    if player == 'WHITE':
        remaining = 16 - state['captures']['BLACK']
        finalResult = (2 * remaining) + (random.uniform(0, 1))
    else:
        remaining = 16 - state['captures']['WHITE']
        finalResult = (2 * remaining) + (random.uniform(0, 1))

    return finalResult


def offensive_eval_1(state, player):
    
    # 2 * (32 - number_of_opponent_pieces_remaining ) + random() .

    if player == 'WHITE':
        return (2 * (state['captures']['WHITE']) + 16) + (random.uniform(0, 1))
    else:
        return (2 * (state['captures']['BLACK']) + 16) + (random.uniform(0, 1))


def defensive_eval_2(state, player):
    wScore = 0  # Current White Score
    bScore = 0  # Current Black Score
    finalScore = 0

    for r_idx, row in enumerate(state['board']):
        for c_idx, col in enumerate(row):

            if col == 'WHITE':
                wScore += (r_idx * r_idx)

            if col == 'BLACK':
                bScore += ((7 - r_idx) * (7 - r_idx))

    if (player == 'WHITE'):
        finalScore = wScore - bScore
    else:
        finalScore = bScore - wScore

    return finalScore


def offensive_eval_2(state, player):
    wScore = 0  # Current White Score
    bScore = 0  # Current Black Score
    finalScore = 0

    for r_idx, row in enumerate(state['board']):
        for c_idx, col in enumerate(row):

            if col == 'WHITE':
                wScore += r_idx * (1 + (r_idx / 15))

            if col == 'BLACK':
                bScore += (7 - r_idx) * (1 + ((7 - r_idx) / 15))

    if (player == 'WHITE'):
        finalScore = wScore - bScore + (5 * (state['captures']['WHITE'] - state['captures']['BLACK']))
    else:
        finalScore = bScore - wScore + (5 * (state['captures']['BLACK'] - state['captures']['WHITE']))

    return finalScore



ag_eval_fn = offensive_eval_2           # ⚠️ Should be enough to pass AG test, but you may change it.
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
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
