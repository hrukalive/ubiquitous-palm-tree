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
    
    def is_valid(self, location, self_pieces):
        within_border = 0 <= location[0] <= 7 and 0 <= location[1] <= 7
        return within_border and location not in self_pieces

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
        # assuming form is (y, x)
        actions = []

        player_turn = state["to_move"]
        
        move_map = {
            'WHITE': [(-1,-1),(-1,0),(-1,1)],
            'BLACK': [(1,-1),(1,0),(1,1)]
        }

        white_locations = []
        black_locations = []

        board = state['board']

        for y in range(len(board)):
            for x in range(len(board[0])):
                position = board[y][x]
                if position == 'WHITE':
                    white_locations.append((y,x))
                elif position == 'BLACK':
                    black_locations.append((y,x))
        piece_map = {
            'WHITE': white_locations,
            'BLACK': black_locations
        }

        opponent_map = {
            'WHITE': black_locations,
            'BLACK': white_locations
        }

        available_moves = move_map[player_turn]

        self_pieces = piece_map[player_turn]
        opponent_pieces = opponent_map[player_turn]

        for piece in piece_map[player_turn]:
            #checking left
            delta_left = available_moves[0]
            left_move = (piece[0]+delta_left[0], piece[1]+delta_left[1])
            if self.is_valid(left_move, self_pieces):
                actions.append({
                    "from": piece,
                    "to": left_move
                })
            delta_right = available_moves[2]
            right_move = (piece[0]+delta_right[0], piece[1]+delta_right[1])
            if self.is_valid(right_move, self_pieces):
                actions.append({
                    "from": piece,
                    "to": right_move
                })
            delta_middle = available_moves[1]
            middle_move = (piece[0]+delta_middle[0], piece[1]+delta_middle[1])
            if self.is_valid(middle_move, self_pieces) and middle_move not in opponent_pieces:
                actions.append({
                    "from": piece,
                    "to": middle_move
                })
            
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

        to_move = state['to_move']
        captures = state['captures'].copy()
        board = [row[:] for row in state['board']]
        piece_current_y,piece_current_x = action['from']
        piece_future_y, piece_future_x = action['to']

        player_map = {
            'BLACK': 'WHITE',
            'WHITE': 'BLACK'
        }

        piece = board[piece_current_y][piece_current_x]

        future_piece = board[piece_future_y][piece_future_x]

        #Assumes that the previous fuctions worked properly and nothing that can't be captured is given to this function
        if future_piece != 'EMPTY':
            captures[to_move] += 1

        #Updating board
        board[piece_future_y][piece_future_x] = piece
        board[piece_current_y][piece_current_x] = 'EMPTY'

        to_move = player_map[to_move]

        return {
            'to_move': to_move,
            'captures': captures,
            'board': board
        }


    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        opponent = 'BLACK' if player == 'WHITE' else 'WHITE'
        
        # Win by reaching last row
        player_win_row = 0 if player == 'WHITE' else 7
        opponent_win_row = 0 if opponent == 'WHITE' else 7
        
        board = state['board']
        
        # Check goal row
        if any(cell == player for cell in board[player_win_row]):
            return 1
        if any(cell == opponent for cell in board[opponent_win_row]):
            return -1
        
        # Check captures (all pieces gone)
        if state['captures'][opponent] == 16:
            return -1
        if state['captures'][player] == 16:
            return 1
        
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state['board']
        players = ['WHITE', 'BLACK']
        player_win_row = {'WHITE': 0, 'BLACK': 7}

        for player in players:
            opponent = 'BLACK' if player == 'WHITE' else 'WHITE'
            # Win by reaching goal row
            if any(cell == player for cell in board[player_win_row[player]]):
                return True
            # Win by capturing all opponent pieces
            if state['captures'][opponent] == 16:
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
    opp_map = {
        'WHITE':'BLACK',
        'BLACK':'WHITE'
    }
    num_pieces = 16 - state['captures'][opp_map[player]]
    
    return 2*num_pieces + random.random()


def offensive_eval_1(state, player):
    num_opp_pieces = (16-state['captures'][player])
    
    return 2*(32-num_opp_pieces) + random.random()


def defensive_eval_2(state, player):
    opp_map = {
        'WHITE':'BLACK',
        'BLACK':'WHITE'
    }
    player_goalie_location = {
        'WHITE':7,
        'BLACK':0
    }

    board = state['board']

    eval = 0
    for y in range(8):
        eval += board[y].count(player) * (y ** 1.5)
    eval += board[player_goalie_location[player]].count(player) * 16
    for y in range(8):
        eval -= board[y].count(opp_map[player]) * (y ** 1.6)
    return eval

def offensive_eval_2(state, player):
    opp_map = {
        'WHITE':'BLACK',
        'BLACK':'WHITE'
    }
    player_goalie_location = {
        'WHITE':7,
        'BLACK':0
    }

    board = state['board']
    
    eval = 0

    for y in range(8):
        eval += board[y].count(player) * (y ** 2)
    eval += (board[player_goalie_location[player]].count(player) + 0.5*(state['captures'][player])) * 16
    for y in range(8):
        eval -= board[y].count(opp_map[player]) * (y ** 1.6)
    return eval


    opp = 'BLACK' if player == 'WHITE' else 'WHITE'
    board = state['board']
    is_white = (player == 'WHITE')
    
    # Directional constants
    forward = -1 if is_white else 1
    my_start_row = 7 if is_white else 0
    opp_start_row = 0 if is_white else 7 # Their home/goalie row
    
    score = 0
    
    # 1. Immediate Victory/Defeat
    if player in board[opp_start_row]: return 1000000
    if opp in board[my_start_row]: return -1000000

    my_pieces = []
    opp_pieces = []
    for y in range(8):
        for x in range(8):
            if board[y][x] == player: my_pieces.append((y, x))
            elif board[y][x] == opp: opp_pieces.append((y, x))

    # 2. Material Advantage
    # We value our pieces more than Def2 values captures to prevent bad trades.
    score += (len(my_pieces) - len(opp_pieces)) * 150

    # 3. Spearhead Strategy (Lead Piece)
    # Def2 scales by y**1.5. We will scale our lead piece by y**4.
    # This forces the AI to commit to a breakthrough rather than moving the whole line.
    max_my_progress = 0
    for y, x in my_pieces:
        progress = abs(y - my_start_row)
        if progress > max_my_progress:
            max_my_progress = progress
        # Standard progress for all pieces
        score += (progress ** 2)

    score += (max_my_progress ** 4)

    # 4. Opponent Threat Management (Paranoia)
    # Def2 scales opponent progress by 1.6. We will scale it by 3.0 to react faster.
    max_opp_progress = 0
    for y, x in opp_pieces:
        opp_progress = abs(y - opp_start_row)
        if opp_progress > max_opp_progress:
            max_opp_progress = opp_progress
        score -= (opp_progress ** 3)

    # 5. Lane Analysis (The Def2 Counter)
    # Def2 keeps goalies on its home row. 
    # We reward pieces that have a "Clear Path" to the goal.
    for y, x in my_pieces:
        path_is_clear = True
        # Check every square from current position to the goal
        for row in range(y + forward, opp_start_row + forward, forward):
            if not (0 <= row < 8): break
            # If there's an opponent directly in front or diagonally able to capture
            for col in [x-1, x, x+1]:
                if 0 <= col < 8 and board[row][col] == opp:
                    path_is_clear = False
                    break
            if not path_is_clear: break
        
        if path_is_clear:
            # Huge bonus for a piece that has effectively "broken" the line
            score += 500 + (abs(y - my_start_row) * 50)

    # 6. Center Bias
    # Pieces in columns 2-5 have more capture/evasion options
    for y, x in my_pieces:
        if 2 <= x <= 5:
            score += 10

    return score

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
    
