import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):

    def __init__(self):
        self.initial = self.initial_state()

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
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|'''
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
        player = state['to_move']
        board = state['board']
        legal_actions = []
        
        # Determine movement direction and identify the enemy
        # White moves from row 7 towards 0 (-1), Black from 0 towards 7 (+1)
        direction = -1 if player == "WHITE" else 1
        enemy = "BLACK" if player == "WHITE" else "WHITE"
        
        for r in range(8):
            for c in range(8):
                # Find pieces belonging to the current player
                if board[r][c] == player:
                    new_r = r + direction
                    
                    # Ensure the new row is within board boundaries
                    if 0 <= new_r < 8:
                        
                        # 1. Straight Forward Move
                        # Rule: Only allowed if the target square is EMPTY
                        if board[new_r][c] == "EMPTY":
                            legal_actions.append({"from": (r, c), "to": (new_r, c)})
                        
                        # 2. Diagonal Forward Moves (Left and Right)
                        # Rule: Allowed if square is EMPTY OR contains an ENEMY (capture)
                        for dc in [-1, 1]:
                            new_c = c + dc
                            if 0 <= new_c < 8:
                                target = board[new_r][new_c]
                                if target == "EMPTY" or target == enemy:
                                    legal_actions.append({"from": (r, c), "to": (new_r, new_c)})
                                    
        return legal_actions

    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        # 1. Create a deep copy of the state to avoid mutating the original
        new_state = deepcopy(state)
        
        board = new_state['board']
        player = new_state['to_move']
        enemy = "BLACK" if player == "WHITE" else "WHITE"
        
        from_r, from_c = action['from']
        to_r, to_c = action['to']
        
        # 2. Check for capture
        # If the destination square contains an enemy, increment the player's capture count
        if board[to_r][to_c] == enemy:
            new_state['captures'][player] += 1
            
        # 3. Update the board
        # The piece moves to the new square, and the old square becomes EMPTY
        board[to_r][to_c] = player
        board[from_r][from_c] = "EMPTY"
        
        # 4. Switch the turn to the other player
        new_state['to_move'] = enemy
        
        return new_state

    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        board = state['board']
        captures = state['captures']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # 1. Check if the current 'player' has won
        # Win by reaching the last row
        win_row = 0 if player == "WHITE" else 7
        if any(board[win_row][c] == player for c in range(8)):
            return 1
        
        # Win by capturing all enemy pieces
        if captures[player] == 16:
            return 1

        # 2. Check if the 'opponent' has won
        # Loss by opponent reaching player's home base
        loss_row = 7 if player == "WHITE" else 0
        if any(board[loss_row][c] == opponent for c in range(8)):
            return -1
        
        # Loss by player losing all pieces
        if captures[opponent] == 16:
            return -1

        return 0
    
    def terminal_test(self, state):

        # Return True if this is a terminal state, False otherwise.
        board = state['board']
        captures = state['captures']

        # 1. Check if all pieces of one color are captured
        # Since each player starts with 16 workers
        if captures['WHITE'] == 16 or captures['BLACK'] == 16:
            return True

        # 2. Check if a worker reached the enemy's home base
        # Check row 0 for any WHITE pieces
        for col in range(8):
            if board[0][col] == "WHITE":
                return True
        
        # Check row 7 for any BLACK pieces
        for col in range(8):
            if board[7][col] == "BLACK":
                return True

        # If none of the above are met, the game continues
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
    """Calculates utility based on the survival of the player's own pieces.
    
    This is a basic defensive heuristic that prioritizes maintaining a high 
    count of workers. It uses a multiplier of 2 to ensure piece count takes 
    precedence over the random tie-breaker.

    Args:
        state (dict): The current game state containing the board and capture counts.
        player (str): The name of the player for whom to calculate utility ("WHITE" or "BLACK").

    Returns:
        float: The calculated utility value.
    """
    opponent = "BLACK" if player == "WHITE" else "WHITE"    
    own_pieces_remaining = 16 - state['captures'][opponent]
    return 2 * own_pieces_remaining + random.random()


def offensive_eval_1(state, player):
    """Calculates utility based on the elimination of the opponent's pieces.
    
    This is a basic aggressive heuristic. It rewards the player for every 
    enemy worker captured. The constant 32 ensures the values remain positive 
    and significant relative to a standard piece count.

    Args:
        state (dict): The current game state.
        player (str): The name of the player for whom to calculate utility.

    Returns:
        float: The calculated utility value.
    """
    opponent_pieces_remaining = 16 - state['captures'][player]    
    return 2 * (32 - opponent_pieces_remaining) + random.random()


def offensive_eval_2(state, player):
    """An advanced aggressive heuristic prioritizing piece differential and advancement.
    
    This strategy focuses on three pillars:
    1. Strongly weights the difference between own and enemy pieces.
    2. Uses a non-linear (squared) bonus for pieces closer to the enemy base.
    3. Provides a massive static bonus for moves that reach the 
       penultimate row, signaling an imminent win.

    Args:
        state (dict): The current game state.
        player (str): The name of the player for whom to calculate utility.

    Returns:
        float: The calculated utility value.
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    own_pieces = 16 - state['captures'][opponent]
    opp_pieces = 16 - state['captures'][player]
    score = 10 * (own_pieces - opp_pieces) 
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                dist = (7 - r) if player == "WHITE" else r
                score += (dist ** 2) * 0.5
                
                if (player == "WHITE" and r == 1) or (player == "BLACK" and r == 6):
                    score += 50 
                    
    return score + random.random()
                

def defensive_eval_2(state, player):
    """An advanced defensive heuristic prioritizing structural integrity and home defense.
    
    This strategy moves beyond simple counting by rewarding:
    1. Bonus for 'Chains' where a piece is protected diagonally 
       from behind by a teammate.
    2. Extra utility for keeping pieces in the initial two home rows.
    3. High base weight on own piece count to discourage risky trades.

    Args:
        state (dict): The current game state.
        player (str): The name of the player for whom to calculate utility.

    Returns:
        float: The calculated utility value.
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    own_pieces = 16 - state['captures'][opponent]
    score = 20 * own_pieces 
    
    direction = -1 if player == "WHITE" else 1
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                home_rows = [6, 7] if player == "WHITE" else [0, 1]
                if r in home_rows:
                    score += 2
                
                back_r = r - direction
                if 0 <= back_r < 8:
                    for dc in [-1, 1]:
                        back_c = c + dc
                        if 0 <= back_c < 8 and board[back_r][back_c] == player:
                            score += 5 
                            
    return score + random.random()


ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.



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
