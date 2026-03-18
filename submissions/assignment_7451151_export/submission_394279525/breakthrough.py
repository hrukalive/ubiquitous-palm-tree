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
        return state['to_move']

    def actions(self, state):
        player = state['to_move']
        board = state['board']
        valid_moves = []
        
        # White moves up (+1), black moves down (-1)
        direction = -1 if player == "WHITE" else 1

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    # Move straight forward (if empty)
                    if 0 <= r + direction < 8:
                        if board[r + direction][c] == "EMPTY":
                            valid_moves.append({"from": (r, c), "to": (r + direction, c)})
                        
                        # Move diagonally forward-left (if empty or enemy)
                        if c - 1 >= 0:
                            target = board[r + direction][c - 1]
                            if target == "EMPTY" or target != player:
                                valid_moves.append({"from": (r, c), "to": (r + direction, c - 1)})
                        
                        # Move diagonally forward-right (if empty or enemy)
                        if c + 1 < 8:
                            target = board[r + direction][c + 1]
                            if target == "EMPTY" or target != player:
                                valid_moves.append({"from": (r, c), "to": (r + direction, c + 1)})
                                
        return valid_moves

    def result(self, state, action):
       # Deepcopy to avoid mutating the parent state
        new_state = deepcopy(state)
        r_from, c_from = action["from"]
        r_to, c_to = action["to"]
        
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Check for capture
        if new_state['board'][r_to][c_to] == opponent:
            new_state['captures'][player] += 1

        # Move piece
        new_state['board'][r_from][c_from] = "EMPTY"
        new_state['board'][r_to][c_to] = player
        
        # Swap turn
        new_state['to_move'] = opponent

        return new_state

    def utility(self, state, player):
        if not self.terminal_test(state):
            return 0
            
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        player_target_row = 0 if player == "WHITE" else 7
        opponent_target_row = 0 if opponent == "WHITE" else 7

        # Check if player won
        if player in state['board'][player_target_row] or state['captures'][player] == 16:
            return 1
            
        # Check if opponent won
        if opponent in state['board'][opponent_target_row] or state['captures'][opponent] == 16:
            return -1
            
        return 0
    
    def terminal_test(self, state):
       # Check capture conditions
        if state['captures']['WHITE'] == 16 or state['captures']['BLACK'] == 16:
            return True
            
        # Check reach end conditions
        if "WHITE" in state['board'][0]:
            return True
        if "BLACK" in state['board'][7]:
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

# Evaluation functions

# 2 * (number_of_own_pieces_remaining) + random()
def defensive_eval_1(state, player):
    own_pieces = get_piece_count(state, player)
    return 2 * own_pieces + random.random()
 
# 2 * (32 - number_of_opponent_pieces_remaining) + random()
def offensive_eval_1(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opponent_pieces = get_piece_count(state, opponent)
    return 2 * (32 - opponent_pieces) + random.random()


def defensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    my_pieces = get_piece_count(state, player)
    opp_pieces = get_piece_count(state, opponent)
    material = my_pieces - opp_pieces
    
    phalanx = phalanx_metric(state, player)
    column = column_metric(state, player)
    reachable_area = reachable_region_area(state, player)
    
    score = (10 * material) + (3 * phalanx) + (3 * column) + (0.5 * reachable_area)
            
    return score + random.random()


def offensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    
    my_pieces = get_piece_count(state, player)
    opp_pieces = get_piece_count(state, opponent)
    material = my_pieces - opp_pieces
    
    progress = runner_progress(state, player)
    runners = runner_count(state, player)
    center = center_control_rows(state, player)
    
    score = (8 * material) + (15 * progress) + (20 * runners) + (2 * center)
            
    return score + random.random()

# Helper Functions for Evaluation 

# Returns player piece count on the board
def get_piece_count(state, player):
    count = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                count += 1
    return count

# Returns the total distance moved by all of player's pieces
def piece_danger_value(state, player):
    score = 0
    home_row = 7 if player == "WHITE" else 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                score += abs(r - home_row)
    return score

# Returns number of pieces in player's home row
def piece_home_row(state, player):
    score = 0
    home_row = 7 if player == "WHITE" else 0
    for c in range(8):
        if state['board'][home_row][c] == player:
            score += 1
    return score

# Retruns number of horizontally connected pieces of the same color
def phalanx_metric(state, player):
    score = 0
    for r in range(8):
        for c in range(7):
            if state['board'][r][c] == player and state['board'][r][c+1] == player:
                score += 1
    return score

# Returns number of pieces on the second to last row that are not under attack
def piece_almost_win(state, player):
    score = 0
    target_row = 0 if player == "WHITE" else 7
    almost_win_row = 1 if player == "WHITE" else 6
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    direction = -1 if player == "WHITE" else 1

    for c in range(8):
        if state['board'][almost_win_row][c] == player:
            under_attack = False
            if c > 0 and state['board'][target_row][c-1] == opponent:
                under_attack = True
            if c < 7 and state['board'][target_row][c+1] == opponent:
                under_attack = True
            
            if not under_attack:
                score += 1
    return score

# Returns number of pieces with no enemy pieces in same or adjacent columns
def runner_count(state, player):
    score = 0
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    direction = -1 if player == "WHITE" else 1
    
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                is_passed = True
                curr_r = r + direction
                while 0 <= curr_r <= 7:
                    if state['board'][curr_r][c] == opponent:
                        is_passed = False; break
                    if c > 0 and state['board'][curr_r][c-1] == opponent:
                        is_passed = False; break
                    if c < 7 and state['board'][curr_r][c+1] == opponent:
                        is_passed = False; break
                    curr_r += direction
                if is_passed:
                    score += 1
    return score

# Returns how close a player is to a breakthrough 
def runner_progress(state, player):
    progress = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                if player == "WHITE":
                    progress = max(progress, 7 - r) 
                else:
                    progress = max(progress, r)      
    return progress

# Retruns score of player's central row positioning score
def center_control_rows(state, player):
    score = 0
    for r in (3, 4):
        for c in range(8):
            if state['board'][r][c] == player:
                score += 1
    return score

# Returns flexibility capacity score of player's pieces
def reachable_region_area(state, player):
    score = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                h = r if player == "WHITE" else 7 - r
                score += 0.5 * (h + 1) * (h + 2)
    return score

# Retruns number of vertically connected player pieces
def column_metric(state, player):
    score = 0
    for r in range(7):
        for c in range(8):
            if state['board'][r][c] == player and state['board'][r+1][c] == player:
                score += 1
    return score

ag_eval_fn = offensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
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
