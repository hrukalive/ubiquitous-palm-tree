from random import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

from simplified_state import *

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
        # Returns the player to move in this state. Possible values: "WHITE" or "BLACK".
        return state['to_move']

    def actions(self, state):
        # Returns a dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        if state['to_move'] == "BLACK":
            direction = 1
            start = 0
            end = 7
        else:
            direction = -1
            start = 1
            end = 8
        actions = []
        for r in range(start, end):
            for c in range(8):
                if state['board'][r][c] == state['to_move']:
                    if c != 0 and state['board'][r + direction][c - 1] != state['to_move']:
                        actions.append({
                            'from': (r, c),
                            'to': (r + direction, c - 1),
                        })
                    if c != 7 and state['board'][r + direction][c + 1] != state['to_move']:
                        actions.append({
                            'from': (r, c),
                            'to': (r + direction, c + 1),
                        })
                    if state['board'][r + direction][c] == "EMPTY":
                        actions.append({
                            'from': (r, c),
                            'to': (r + direction, c),
                        })
        return actions

    def result(self, state, action):
        # Returns the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        current = state['to_move']
        opponent = "BLACK" if current == "WHITE" else "WHITE" 
        captures = deepcopy(state['captures'])
        if state['board'][action['to'][0]][action['to'][1]] == opponent:
            captures[current] += 1
        board = deepcopy(state['board'])
        board[action['to'][0]][action['to'][1]] = current
        board[action['from'][0]][action['from'][1]] = "EMPTY" 
        return {
            'to_move': opponent,
            'captures': captures,
            'board': board,
        }

    def utility(self, state, player):
        # Returns the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if player == "WHITE":
            output = 1
        else:
            output = -1
        for c in range(8):
            if state['board'][0][c] == "WHITE":
                return output
            if state['board'][7][c] == "BLACK":
                return -1 * output
        if state['captures']['WHITE'] == 16:
            return output
        if state['captures']['BLACK'] == 16:
            return -1 * output
        return 0


    def terminal_test(self, state):
        # Returns True if this is a terminal state, False otherwise.
        return self.utility(state, "WHITE") != 0

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


def defensive_eval_1(state):
    '''Own piece count'''
    board = state['board']
    turn = state['to_move']
    n = 0
    for r in range(8):
        for c in range(8):
            s = board[r][c]
            if s == turn:
                n += 1
    return 2 * n + random()


def offensive_eval_1(state):
    '''Opponent piece count'''
    board = state['board']
    turn = state['to_move']
    n = 0
    for r in range(8):
        for c in range(8):
            s = board[r][c]
            if s != turn and s != "EMPTY":
                n += 1
    return 2 * (32 - n) + random()


def defensive_eval_2(state):
    '''Piece Majority'''
    board = state['board']
    val = 0
    for r in range(8):
        for c in range(8):
            s = board[r][c]
            if s == "WHITE":
                val += 62
            elif s == "BLACK":
                val -= 62
    return val


def defensive_eval_3(state):
    '''Piece Positioning'''
    table = [
        [857, 857, 857, 857, 857, 857, 857, 857],
        [750, 821, 821, 821, 821, 821, 821, 750],
        [500, 786, 786, 786, 786, 786, 786, 500],
        [321, 536, 750, 750, 750, 750, 750, 321],
        [214, 321, 571, 571, 571, 571, 321, 214],
        [107, 179, 357, 357, 357, 357, 179, 107],
        [ 71, 107, 107, 107, 107, 107, 107,  71],
        [179,1000,1000, 429, 429,1000,1000, 179],
    ]
    board = state['board']
    n = 0
    val = 0 
    for r in range(8):
        for c in range(8):
            s = board[r][c]
            if s == "WHITE":
                val += table[r][c]
                n += 1
            elif s == "BLACK":
                val -= table[7 - r][c]
                n += 1
    return val / n


def offensive_eval_2(state):
    '''Endgame''' 
    white, black = simplify_state(state)
    whites_turn = 1 if state['to_move'] == "WHITE" else 0 
    
    if white & 0x00000000000000FF: return 1000
    if black & 0xFF00000000000000: return -1000

    white_left = ((white & 0x00FEFEFEFEFEFEFEFE) >> 9)
    white_right = ((white & 0x007F7F7F7F7F7F7F7F) >> 7)
    black_left = ((black & 0x00FEFEFEFEFEFEFEFE) << 7)
    black_right = ((black & 0x007F7F7F7F7F7F7F7F) << 9)

    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_control = (white_any &~ black_any) | (white_both &~ black_both)
    black_control = (black_any &~ white_any) | (black_both &~ white_both)
    safe_white = 0xFFFFFFFFFFFFFFFF &~ black_control
    safe_black = 0xFFFFFFFFFFFFFFFF &~ white_control
    
    if whites_turn: 
        if white & 0x000000000000FF00:
            return 1000.0
        if safe_black & black & 0x00FF000000000000:
            return -1000.0   
    else: 
        if black & 0x00FF000000000000:
            return -1000.0
        if safe_white & white & 0x000000000000FF00:
            return 1000.0
    return 0.0


def offensive_eval_3(state):
    '''Attackers v Guarders'''
    white, black = simplify_state(state)
    pieces = white | black
    white_left = (((white & 0x00FEFEFEFEFEFEFEFE) >> 9) & pieces)
    white_right = (((white & 0x007F7F7F7F7F7F7F7F) >> 7) & pieces)
    black_left = (((black & 0x00FEFEFEFEFEFEFEFE) << 7) & pieces)
    black_right = (((black & 0x007F7F7F7F7F7F7F7F) << 9) & pieces)
    
    white_any = white_left | white_right
    white_both = white_left & white_right
    black_any = black_left | black_right
    black_both = black_left & black_right
    
    white_wins = (white_any &~ black_any) | (white_both &~ black_both)
    black_wins = (black_any &~ white_any) | (black_both &~ white_both)
    
    return 31 * (bin(white_wins).count('1') - bin(black_wins).count('1'))

def combined_eval(state):
    return (10.0 * offensive_eval_2(state)) + \
           (0.9 * defensive_eval_2(state)) + \
           (0.1 * defensive_eval_3(state))

from evaluators import evaluator_4
ag_eval_fn = evaluator_4           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = evaluator_4  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
        'final_state': state,
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)

