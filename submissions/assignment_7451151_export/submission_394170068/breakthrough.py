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
        return state["to_move"]
    
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
        direction = -1 if player == "WHITE" else 1
        inv_color = lambda x: "WHITE" if x == "BLACK" else "BLACK"
        def individual_action(row,col):
            col_deltas = [-1,0,1]
            moves = []
            for dj in col_deltas:
                new_row = row+direction
                new_col = col+dj
                if new_row < 0 or new_row > 7: continue
                if new_col < 0 or new_col > 7: continue
                if state["board"][new_row][new_col] == player: continue
                if state["board"][new_row][new_col] == inv_color(player) and dj == 0: continue
                moves.append({"from":(row,col), "to":(new_row,new_col)})
            return moves
        available_actions = []
        for i in range(8):
            for j in range(8):
                if state["board"][i][j] == player:
                    moves = individual_action(i,j)
                    available_actions = available_actions + moves
        return available_actions
            

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
        resultant_state = deepcopy(state)
        inv_color = lambda x: "WHITE" if x == "BLACK" else "BLACK"
        start = action["from"]
        to = action["to"]
        if state["board"][to[0]][to[1]] != "EMPTY":

            captured = inv_color(state["board"][to[0]][to[1]])
            resultant_state["captures"][captured] += 1
        resultant_state["to_move"] = inv_color( state["to_move"])
        resultant_state["board"][start[0]][start[1]] = "EMPTY"
        resultant_state["board"][to[0]][to[1]] = state["to_move"]
            
        
        return resultant_state

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        good_for = lambda winning_player: 100_000_000 if winning_player == player else -100_000_000
        if state["captures"]["BLACK"] == 16:
            return good_for("BLACK")
        elif state["captures"]["WHITE"] == 16:
            return good_for("WHITE")
        for bottom_row,top_row in zip(state["board"][7],state["board"][0]):
            if bottom_row == "BLACK":
                return good_for("BLACK")
            elif top_row == "WHITE":
                return good_for("WHITE")
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        
        return self.utility(state,"WHITE") != 0
        

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
import numpy as np

def phi(state, player):
    """
    Features:
    0 own_pieces_remaining
    1 opponent_pieces_remaining
    2 avg_pawn_advancement
    3 threatened_captures
    4 mobility
    5 min_distance_to_promotion
    6 center_control
    7 bias
    """

    other_player = "BLACK" if player == "WHITE" else "WHITE"

    own_pieces_remaining = 16 - state["captures"][player]
    opponent_pieces_remaining = 16 - state["captures"][other_player]

    avg_pawn_advancement = 0
    min_distance_to_promotion = 8
    threatened_captures = 0
    mobility = 0
    center_control = 0

    direction = -1 if player == "WHITE" else 1
    CENTER_COLS = {2, 3, 4, 5}

    def inv_color(c):
        return "BLACK" if c == "WHITE" else "WHITE"

    def individual_actions(row, col):
        nonlocal threatened_captures
        moves = 0

        for dj in [-1, 0, 1]:
            new_row = row + direction
            new_col = col + dj

            if new_row < 0 or new_row > 7: continue
            if new_col < 0 or new_col > 7: continue

            target = state["board"][new_row][new_col]

            if dj == 0:
                if target == "EMPTY":
                    moves += 1
            else:
                if target == inv_color(player):
                    threatened_captures += 1
                    moves += 1

        return moves

    for i in range(8):
        for j in range(8):
            if state["board"][i][j] == player:

                if player == "WHITE":
                    advancement = 7 - i
                    distance = i
                else:
                    advancement = i
                    distance = 7 - i

                avg_pawn_advancement += advancement
                min_distance_to_promotion = min(min_distance_to_promotion, distance)

                if j in CENTER_COLS:
                    center_control += 1

                mobility += individual_actions(i, j)

    avg_pawn_advancement /= max(1, own_pieces_remaining)

    features = np.array([
        own_pieces_remaining,
        opponent_pieces_remaining,
        avg_pawn_advancement,
        threatened_captures,
        mobility,
        min_distance_to_promotion,
        center_control,
        1.0
    ])

    return features

def defensive_eval_1(state, player):
    features = phi(state,player)
    W = np.zeros_like(features)
    W[0] = 2
    eval = features @ W.T + random.random()
    return eval


def offensive_eval_1(state, player):
    features = phi(state,player)
    W = np.zeros_like(features)
    W[1] = -2
    W[-1] = 64
    eval = features @ W.T + random.random()
    return eval


def defensive_eval_2(state, player):
    features = phi(state,player)
    W = np.array([-2.97735126,  2.70103511, -2.91533548, -0.69935598,  1.49179858, -1.6877506,  0.48682123, -5.42452899])
    # W = np.array([-10.5091599,    5.75224727,  -4.40468067,  -0.46920749,   2.85472434,  -4.04706817,  -0.48548426,  -5.95340843])
    # W = np.array([0.8,-2.5, 2.0, 3.5, 1.5, -3.5, 1.0, 0.5 ])
    # W = np.array([1.2,-1.8,2.5,2.5,1.8,-4.0,2.0,0.5])
    eval = features @ W.T + 0.1*random.random()
    return eval


def offensive_eval_2(state, player):
    features = phi(state,player)
    W = np.array([-5.82664428,  1.06427708, -0.90816662, -1.30766562,  1.37431272, -2.95610787, -0.55881905,  0.75327318])
    # W = np.array([1.0, -0.5, 3.0, 1.5, 2.0, -4.5, 2.5, 0.5])
    eval = features @ W.T + 0.1*random.random()
    return eval

# def gmo_agent(state,player):
#     features = phi(state,player)
#     # W = np.array([-10.5091599,    5.75224727,  -4.40468067,  -0.46920749,   2.85472434,  -4.04706817,  -0.48548426,  -5.95340843])
#     W = np.array([-2.97735126,  2.70103511, -2.91533548, -0.69935598,  1.49179858, -1.6877506,  0.48682123, -5.42452899])
#     eval = features @ W.T + 0.1*random.random()
#     return eval

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
