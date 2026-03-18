import random
from copy import deepcopy

import numpy.random
from tqdm import tqdm
from games import Game
from src.breakthrough_agent import RandomAgent


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
        actions = []
        for r in range(0, 8):
            for c in range(0,8):
                if state['board'][r][c] == state['to_move'] and state['to_move'] == "BLACK":
                    space1 = state['board'][r+1][c-1] if (r < 7) and (c > 0) else -1
                    space2 = state['board'][r+1][c] if (r < 7) else -1
                    space3 = state['board'][r+1][c+1] if (r < 7) and (c < 7) else -1
                    if space1 == "WHITE":
                        actions.append({"from": (r,c),
                                        "to": (r+1,c-1)})
                    if space2 == "EMPTY":
                        actions.append({"from": (r,c),
                                        "to": (r+1,c)})
                    if space3 == "WHITE":
                        actions.append({"from": (r,c),
                                        "to": (r+1,c+1)})
                if state['board'][r][c] == state['to_move'] and state['to_move'] == "WHITE":
                    space1 = state['board'][r-1][c-1] if (r > 0) and (c > 0) else -1
                    space2 = state['board'][r-1][c] if (r > 0) else -1
                    space3 = state['board'][r-1][c+1] if (r > 0) and (c < 7) else -1
                    if space1 == "BLACK":
                        actions.append({"from": (r,c),
                                        "to": (r-1,c-1)})
                    if space2 == "EMPTY":
                        actions.append({"from": (r,c),
                                        "to": (r-1,c)})
                    if space3 == "BLACK":
                        actions.append({"from": (r,c),
                                        "to": (r-1,c+1)})
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

        if action is None:
            new_state = deepcopy(state)
            new_state['to_move'] = 'WHITE' if state['to_move'] == 'BLACK' else 'BLACK'
            return new_state

        # Get old piece location
        prev = action['from']

        # Get the new piece location
        new = action['to']

        new_captures = 0
        player = state['to_move']
        new_spot = state['board'][new[0]][new[1]]

        new_state = deepcopy(state)
        if player == "WHITE" and new_spot == "BLACK":
            new_state['captures']["WHITE"] = state['captures']["WHITE"] + 1
        elif player == "BLACK" and new_spot == "WHITE":
            new_state['captures']["BLACK"] = state['captures']["BLACK"] + 1

        new_state['board'][new[0]][new[1]] = state['to_move']
        new_state['board'][prev[0]][prev[1]] = "EMPTY"
        new_state['to_move'] = 'WHITE' if state['to_move'] == 'BLACK' else 'BLACK'
        # print(new_state)
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
        white_pieces = 0
        black_pieces = 0

        pos_util = 2000
        neg_util = -2000

        # Count each piece for both players, and check for win
        for r in range(0,8):
            for c in range(0, 8):
                if r == 0:
                    if state['board'][0][c] == 'WHITE':
                        utility = pos_util if player == 'WHITE' else neg_util
                        return utility
                if r == 7:
                    if(state['board'][7][c]) == 'BLACK':
                        utility = pos_util if player == 'BLACK' else neg_util
                        return utility
                if state['board'][r][c] == 'WHITE':
                    white_pieces += 1
                if state['board'][r][c] == 'BLACK':
                    black_pieces += 1

        # Check if all of white's pieces have been captured
        if white_pieces == 0:
            return pos_util if player == 'BLACK' else neg_util

        # Check if all of black's pieces have been captured
        if black_pieces == 0:
            return pos_util if player == 'WHITE' else neg_util

        # Otherwise, return mid utility
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.

        white_pieces = 0
        black_pieces = 0

        # Count each piece for both players, and check for win
        for r in range(0, 8):
            for c in range(0, 8):
                if r == 0:
                    if state['board'][0][c] == 'WHITE':
                        return True
                if r == 7:
                    if (state['board'][7][c]) == 'BLACK':
                        return True
                if state['board'][r][c] == 'WHITE':
                    white_pieces += 1
                if state['board'][r][c] == 'BLACK':
                    black_pieces += 1
        return (white_pieces == 0) or (black_pieces == 0)

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
    pieces = 0
    for r in range(0, 8):
        for c in range(0, 8):
            if state['board'][r][c] == player:
                pieces += 1
    return 2 * pieces + numpy.random.random()

def offensive_eval_1(state, player):
    return 2 * (32 - state['captures'][player]) + numpy.random.random()

# Prioritize blocking enemy pieces
def defensive_eval_2(state, player):
    eval = 0
    for c in range(0, 8):
        for r in range(0, 7):
            enemyPlayer = state['board'][r][c] != player and state['board'][r][c] != "EMPTY"
            if player == "WHITE" and enemyPlayer:
                eval += 50 if state['board'][r+1][c] == "WHITE" else 0
            elif player == "BLACK" and enemyPlayer:
                eval += 50 if state['board'][r-1][c] == "BLACK" else 0
    return eval

# Prioritize moving pieces forward
def offensive_eval_2(state, player):
    start = 0 if player == 'WHITE' else 7
    end = 7 if player == 'WHITE' else 0
    step = 1 if player == 'WHITE' else -1
    mult = 10
    eval = 0
    for r in range(start, end, step):
        if player in state['board'][r]:
            eval += mult * (r - 2) if player == 'BLACK' else mult * (5 - r)
    return eval + random.random()

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

    '''
    ........
    .BBBBBBB
    .B.BBBBB
    BBB....W
    .W..W.WW
    ..W...WW
    ....WW..
    WWWWW...
    '''
    game = Breakthrough()
    testBoard = [["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"], # 0
                 ["BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK"], # 1
                 ["EMPTY","WHITE","EMPTY","BLACK","BLACK","BLACK","BLACK","BLACK"], # 2
                 ["BLACK","BLACK","BLACK","WHITE","EMPTY","EMPTY","EMPTY","EMPTY"], # 3
                 ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"], # 4
                 ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"], # 5
                 ["WHITE","EMPTY","WHITE","WHITE","WHITE","WHITE","WHITE","WHITE"], # 6
                 ["WHITE","WHITE","WHITE","WHITE","WHITE","WHITE","WHITE","WHITE"]] # 7

    white_agent = AlphaBetaAgent("AB1",depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=defensive_eval_2)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
