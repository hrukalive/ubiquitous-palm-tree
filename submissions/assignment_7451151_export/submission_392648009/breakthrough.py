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
        moves = []
        player = self.to_move(state)
        grid = state['board']
        for r in range(8):
            for c in range(8):
                if grid[r][c] == player:
                    # Check all possible moves for this piece
                    if player == "WHITE":
                        # White moves up (towards row 0)
                        if r > 0 and grid[r-1][c] == "EMPTY":
                            moves.append({"from": (r, c), "to": (r-1, c)})
                        # Diagonal captures
                        if r > 0 and c > 0 and grid[r-1][c-1] != "WHITE":
                            moves.append({"from": (r, c), "to": (r-1, c-1)})
                        if r > 0 and c < 7 and grid[r-1][c+1] != "WHITE":
                            moves.append({"from": (r, c), "to": (r-1, c+1)})
                    else:
                        # Black moves down (towards row 7)
                        if r < 7 and grid[r+1][c] == "EMPTY":
                            moves.append({"from": (r, c), "to": (r+1, c)})
                        # Diagonal captures
                        if r < 7 and c > 0 and grid[r+1][c-1] != "BLACK":
                            moves.append({"from": (r, c), "to": (r+1, c-1)})
                        if r < 7 and c < 7 and grid[r+1][c+1] != "BLACK":
                            moves.append({"from": (r, c), "to": (r+1, c+1)})
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
        new_state = deepcopy(state)
        player = self.to_move(state)
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        from_r, from_c = action["from"]
        to_r, to_c = action["to"]
        # Move the piece
        new_state['board'][to_r][to_c] = player
        new_state['board'][from_r][from_c] = "EMPTY"
        # Check for capture
        if state['board'][to_r][to_c] == opponent:
            new_state['captures'][player] += 1
        # Update to_move
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
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        # Check if player has won
        for c in range(8):
            if state['board'][0][c] == "WHITE":
                return 1 if player == "WHITE" else -1
            if state['board'][7][c] == "BLACK":
                return 1 if player == "BLACK" else -1
        if(state['captures'][player] == 16):
            return 1
        if(state['captures'][opponent] == 16):
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
        return self.utility(state, self.to_move(state)) != 0
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
    own_pieces = 16 - state['captures'][("BLACK" if player == "WHITE" else "WHITE")]
    return 2 * own_pieces + random.random()
    



def offensive_eval_1(state, player):
    
    
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opponent_pieces = 16 - state['captures'][player]
    return 2 * (32 - opponent_pieces) + random.random()

def defensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state['board']
    score = 0
    
    own_pieces = 16 - state['captures'][opponent]
    opponent_pieces = 16 - state['captures'][player]
    
    # Scarcity bonus - each piece worth more as you lose pieces
    scarcity_bonus = (17 - own_pieces)
    score += own_pieces * scarcity_bonus
    
    # Column spread bonus
    own_columns = set(c for r in range(8) for c in range(8) if board[r][c] == player)
    score += len(own_columns) * 2
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                if opponent == "WHITE":
                    advancement = 7 - r
                    path_clear = all(board[row][c] != player for row in range(r-1, -1, -1))
                else:
                    advancement = r
                    path_clear = all(board[row][c] != player for row in range(r+1, 8))
                
                # Penalize enemy advancement
                if advancement >= 5:
                    score -= advancement * 5
                elif advancement >= 3:
                    score -= advancement * 2
                else:
                    score -= advancement
                # Big penalty if opponent is one step from winning
                if advancement >= 6:
                    score -= 100
            
            if board[r][c] == player:
                if player == "WHITE":
                    advancement = 7 - r
                    threat_row = r + 1
                    protect_row = r + 1
                else:
                    advancement = r
                    threat_row = r - 1
                    protect_row = r - 1
                
                # Small reward for own advancement
                score += advancement * 0.5
                
                # Center control bonus
                if 2 <= c <= 5:
                    score += 1.5
                
                # Big bonus if one step from winning
                if advancement >= 6:
                    score += 100
                
                # Penalize if advanced piece is threatened
                if advancement >= 5 and 0 <= threat_row <= 7:
                    if c > 0 and board[threat_row][c-1] == opponent:
                        score -= advancement * 3
                    if c < 7 and board[threat_row][c+1] == opponent:
                        score -= advancement * 3
                
                # Protected piece bonus - friendly piece diagonally behind
                if 0 <= protect_row <= 7:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc <= 7 and board[protect_row][nc] == player:
                            score += advancement * 2  # more valuable the further advanced
    
    return score + random.random()


def offensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state['board']
    score = 0
    
    own_pieces = 16 - state['captures'][opponent]
    opponent_pieces = 16 - state['captures'][player]
    
    # Prioritize capturing
    score += (16 - opponent_pieces) * 3
    
    # Avoid bad trades
    if own_pieces < opponent_pieces:
        score -= (opponent_pieces - own_pieces) * 4
    
    threat_columns = set()
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    advancement = 7 - r
                    threat_row = r + 1
                else:
                    advancement = r
                    threat_row = r - 1
                
                # Reward advancement exponentially
                score += advancement ** 2
                
                # Big bonus if one step from winning
                if advancement >= 6:
                    score += 200
                
                # Center control
                if 2 <= c <= 5:
                    score += 1.5
                
                # Track columns with advanced pieces
                if advancement >= 4:
                    threat_columns.add(c)
                
                # Bonus for clear path ahead
                if player == "WHITE":
                    path_clear = all(board[row][c] == "EMPTY" for row in range(r-1, -1, -1))
                else:
                    path_clear = all(board[row][c] == "EMPTY" for row in range(r+1, 8))
                
                if path_clear and advancement >= 3:
                    score += advancement * 5
                
                # Protect advanced pieces from being captured
                if advancement >= 5 and 0 <= threat_row <= 7:
                    if c > 0 and board[threat_row][c-1] == opponent:
                        score -= advancement * 3
                    if c < 7 and board[threat_row][c+1] == opponent:
                        score -= advancement * 3
            
            # Penalize dangerous enemy pieces
            if board[r][c] == opponent:
                if opponent == "WHITE":
                    enemy_advancement = 7 - r
                    attack_row = r - 1
                else:
                    enemy_advancement = r
                    attack_row = r + 1
                
                score -= enemy_advancement * 2
                
                
    # Multi-threat bonus
    if len(threat_columns) >= 2:
        score += len(threat_columns) * 15
    
    # Piece advantage bonus
    if own_pieces > opponent_pieces:
        score += (own_pieces - opponent_pieces) * 5
    
    
    return score + random.random()

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
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
