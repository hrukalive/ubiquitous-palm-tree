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
        actions = []
        grid = state['board']
        player = self.to_move(state)
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        
        # Direction of movement: White moves up (r-1), Black moves down (r+1)
        direction = -1 if player == "WHITE" else 1
        
        for r in range(8):
            for c in range(8):
                if grid[r][c] == player:
                    # 1. Straight move (Must be EMPTY)
                    nr, nc = r + direction, c
                    if 0 <= nr < 8:
                        if grid[nr][nc] == "EMPTY":
                            actions.append({"from": (r, c), "to": (nr, nc)})
                    
                    # 2. Diagonal moves (Can be EMPTY or OPPONENT)
                    for dc in [-1, 1]:
                        nr, nc = r + direction, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            # In Breakthrough, you can move diagonally to an empty square 
                            # OR capture an opponent. You just can't capture your own piece.
                            if grid[nr][nc] != player:
                                actions.append({"from": (r, c), "to": (nr, nc)})
        return actions

    def result(self, state, action):
        new_state = deepcopy(state)
        
        start_r, start_c = action["from"]
        end_r, end_c = action["to"]
        player = new_state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        if new_state['board'][end_r][end_c] == opponent:
            new_state['captures'][player] += 1

        new_state['board'][start_r][start_c] = "EMPTY"
        new_state['board'][end_r][end_c] = player

        new_state['to_move'] = opponent
        
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
        grid = state['board']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        
        white_won = "WHITE" in grid[0] or sum(row.count("BLACK") for row in grid) == 0
        black_won = "BLACK" in grid[7] or sum(row.count("WHITE") for row in grid) == 0

        if player == "WHITE":
            if white_won: return 1000
            if black_won: return -1000
        else:
            if black_won: return 1000
            if white_won: return -1000
            
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        grid = state['board']
        if "WHITE" in grid[0]:
            return True
        if "BLACK" in grid[7]:
            return True
        
        white_count = sum(row.count("WHITE") for row in grid)
        black_count = sum(row.count("BLACK") for row in grid)
        
        return white_count == 0 or black_count == 0        

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
    grid = state['board']
    my_pieces = sum(row.count(player) for row in grid)
    opp = "BLACK" if player == "WHITE" else "WHITE"
    opp_pieces = sum(row.count(opp) for row in grid)
    # Pure material advantage
    return my_pieces - opp_pieces


def offensive_eval_1(state, player):
    grid = state['board']
    score = 0
    for r in range(8):
        for c in range(8):
            if grid[r][c] == player:
                score += 10  # Base value for having a piece
                # Add points for how far advanced the piece is
                dist = (7 - r) if player == "WHITE" else r
                score += dist 
            elif grid[r][c] != "EMPTY":
                score -= 10  # Subtract points for opponent pieces
    return score


def defensive_eval_2(state, player):
    grid = state['board']
    score = 0
    direction = 1 if player == "WHITE" else -1 # Check rows "behind"
    
    for r in range(8):
        for c in range(8):
            if grid[r][c] == player:
                score += 5
                # Check for support from pieces diagonally behind
                for dc in [-1, 1]:
                    nr, nc = r + direction, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if grid[nr][nc] == player:
                            score += 2 # Bonus for being protected
    return score


def offensive_eval_2(state, player):
    grid = state['board']
    score = 0
    for r in range(8):
        for c in range(8):
            if grid[r][c] == player:
                dist = (7 - r) if player == "WHITE" else r
                score += (dist ** 2) # Exponential reward for progress
    return score

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
