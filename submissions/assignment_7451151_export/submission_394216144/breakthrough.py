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
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]        
        moves = []
        current_player = state['to_move']
        board = state['board']
        
        # Determine direction: WHITE moves up (row decreases), BLACK moves down (row increases)
        direction = -1 if current_player == "WHITE" else 1
        
        # Find all pieces belonging to current player
        for r in range(8):
            for c in range(8):
                if board[r][c] == current_player:
                    # Check three possible moves: forward-left, forward, forward-right
                    new_row = r + direction
                    
                    # Make sure new_row is valid
                    if 0 <= new_row < 8:
                        # Forward-left diagonal
                        if c - 1 >= 0:
                            target = board[new_row][c - 1]
                            # Can move if empty or enemy piece (capture)
                            if target == "EMPTY" or target != current_player:
                                moves.append({"from": (r, c), "to": (new_row, c - 1)})
                        
                        # Forward straight
                        target = board[new_row][c]
                        # Can only move forward if empty (no capture straight ahead)
                        if target == "EMPTY":
                            moves.append({"from": (r, c), "to": (new_row, c)})
                        
                        # Forward-right diagonal
                        if c + 1 < 8:
                            target = board[new_row][c + 1]
                            # Can move if empty or enemy piece (capture)
                            if target == "EMPTY" or target != current_player:
                                moves.append({"from": (r, c), "to": (new_row, c + 1)})
        
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
        # Create a deep copy so we don't modify the original state
        new_state = deepcopy(state)
        
        from_r, from_c = action['from']
        to_r, to_c = action['to']
        
        current_player = new_state['to_move']
        
        # Check if this move captures an enemy piece
        if new_state['board'][to_r][to_c] != "EMPTY":
            new_state['captures'][current_player] += 1
        
        # Move the piece
        new_state['board'][to_r][to_c] = new_state['board'][from_r][from_c]
        new_state['board'][from_r][from_c] = "EMPTY"
        
        # Switch to the other player
        new_state['to_move'] = "BLACK" if current_player == "WHITE" else "WHITE"
        
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
        if not self.terminal_test(state):
            return 0
        
        # If terminal, determine who won
        # Check if player reached their goal
        if player == "WHITE":
            # WHITE wins if any WHITE piece is in row 0
            for c in range(8):
                if state['board'][0][c] == "WHITE":
                    return 1000  # WIN
        else:  # player == "BLACK"
            # BLACK wins if any BLACK piece is in row 7
            for c in range(8):
                if state['board'][7][c] == "BLACK":
                    return 1000  # WIN
        
        # If it's terminal but player didn't win, they lost
        return -1000

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.        
        # Check if WHITE reached row 0 (top) - WHITE wins
        for c in range(8):
            if state['board'][0][c] == "WHITE":
                return True
        
        # Check if BLACK reached row 7 (bottom) - BLACK wins
        for c in range(8):
            if state['board'][7][c] == "BLACK":
                return True
        
        # Check if current player has no legal moves - current player loses
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
    # Simple evaluation: count pieces and favor having more pieces
    board = state['board']
    my_pieces = 0
    opponent_pieces = 0
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
            elif board[r][c] == opponent:
                opponent_pieces += 1
    
    # Simple material count difference
    return my_pieces - opponent_pieces


def offensive_eval_1(state, player):
    # 30% piece count, 70% distance to goal
    board = state['board']
    my_pieces = 0
    opponent_pieces = 0
    my_advancement = 0
    
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
                # WHITE goal is row 0 (top), BLACK goal is row 7 (bottom)
                if player == "WHITE":
                    # Lower row number = closer to goal (0 is best)
                    # Advancement score: 7-r (piece at row 0 gets 7, row 7 gets 0)
                    my_advancement += (7 - r)
                else:  # BLACK
                    # Higher row number = closer to goal (7 is best)
                    # Advancement score: r (piece at row 7 gets 7, row 0 gets 0)
                    my_advancement += r
            elif board[r][c] == opponent:
                opponent_pieces += 1
    
    # 30% material advantage, 70% advancement
    material = my_pieces - opponent_pieces
    advancement = my_advancement  # Already summed up
    
    return 0.3 * material + 0.7 * advancement


def defensive_eval_2(state, player):
    # 70% survival (very defensive), 30% advancement
    board = state['board']
    my_pieces = 0
    opponent_pieces = 0
    my_advancement = 0
    
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
                if player == "WHITE":
                    my_advancement += (7 - r)
                else:
                    my_advancement += r
            elif board[r][c] == opponent:
                opponent_pieces += 1
    
    # 70% material (defensive), 30% advancement
    material = my_pieces - opponent_pieces
    return 0.7 * material + 0.3 * my_advancement


def offensive_eval_2(state, player):
    # 10% survival, 90% advancement (very aggressive)
    board = state['board']
    my_pieces = 0
    opponent_pieces = 0
    my_advancement = 0
    
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                my_pieces += 1
                if player == "WHITE":
                    my_advancement += (7 - r)
                else:
                    my_advancement += r
            elif board[r][c] == opponent:
                opponent_pieces += 1
    
    # 10% material, 90% advancement (all-out attack!)
    material = my_pieces - opponent_pieces
    return 0.1 * material + 0.9 * my_advancement

ag_eval_fn = offensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
