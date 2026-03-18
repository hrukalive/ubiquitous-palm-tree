import random
from copy import deepcopy

import numpy as np
# from pygame.examples import grid
from tqdm import tqdm
from copy import deepcopy
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
        return state["to_move"]

    def actions(self, state):
        #Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        grid = state["board"]
        actions = []
        cur_player = state['to_move']
        for r in range(8):
            for c in range(8):
                if grid[r][c] == cur_player: #only show moves for current player
                    #find legal moves for this piece
                    moves = self._moves(grid, grid[r][c], r, c)
                    # print("moves from", (r, c), "are", moves)
                    if moves:
                        for move in moves:
                            actions.append({"from": (r, c), "to": move })
        return actions

    def result(self, state, action):
        new_state = deepcopy(state) #important!
        #result function should alternate the player because the
        # -resulting board's to_move should be the opponent of current board's player.
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        cur_player = new_state['to_move']
        to_tile = new_state["board"] [action["to"][0]] [action["to"][1]]
        from_tile = new_state["board"] [action["from"][0]] [action["from"][1]]


        if to_tile != cur_player and to_tile != "EMPTY":
            new_state["captures"][cur_player] += 1 # a capture
        new_state["board"] [action["to"][0]] [action["to"][1]] = cur_player #put current players color piece in new spot
        new_state["board"] [action["from"][0]] [action["from"][1]]= "EMPTY" #set empty as leaving space

        new_state["to_move"] = ("BLACK" if new_state["to_move"] == "WHITE" else "WHITE")
        # print("turn:", new_state["to_move"])
        return new_state


    def utility(self, state, player, depth):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        winner = self._winner(state["board"])
        if winner is None:
            return 0
        #below line: Prioritize early win (eg win in 2 moves vs win in 4 moves)
        return 1000000 - depth if winner == player else -1000000 + depth #make this very wanted


    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        return "WHITE" in state["board"][0] or "BLACK" in state["board"][7]


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

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _moves(self, grid, color, row, col):
        tile_move = ()
        moves = []
        for i in range(-1, 2): #-1, 0, 1
            if color == "WHITE":
                tile_move = self._validMove(grid, color, row, col, row - 1, col + i)
            elif color == "BLACK":
                # print("_moves cell", (row,col),"looking at", (row + 1, col + i))
                tile_move = self._validMove(grid, color, row, col, row + 1, col + i)
            if tile_move:
                moves.append(tile_move)
        return moves

    def _validMove(self, grid, color, row, col, new_row, new_col):
        if (0 <= new_row < 8) and (0 <= new_col < 8):
            if new_col != col and grid[new_row][new_col] != color: #if empty or other color?
                return tuple((new_row, new_col)) #move diagonal or capture
            elif new_col == col and grid[new_row][col] == "EMPTY": #cant move forward if blocked
            # print("tuple:",tuple((row,col)))
                return tuple((new_row, new_col)) #move forwards
        # print("invalid cell:", (row,col))
        return None

    def _winner(self, grid):
        return "WHITE" if "WHITE" in grid[0] else ("BLACK" if "BLACK" in grid[7] else None)

##################################################
# Evaluation functions

def defensive_eval_1(state, player):
    num_pieces = 0
    for row in state["board"]:
        for tile in row:
            if tile == player:
                num_pieces += 1
    return  2 * num_pieces + random.random()


def offensive_eval_1(state, player):
    num_opponent_pieces = 0
    for row in state["board"]:
        for tile in row:
            if tile != player and tile != "EMPTY": #other players pieces
               num_opponent_pieces += 1
    return 2 * (32 - num_opponent_pieces) + random.random()

def net_eval(state, player): #ADDED EXTRA for fun
    num_pieces = 0
    num_opponent_pieces = 0
    for row in state["board"]:
        for tile in row:
            if tile != player and tile != "EMPTY": num_opponent_pieces += 1
            if tile == player: num_pieces += 1
    return 2 * (num_pieces - num_opponent_pieces) + random.random()


###############-----SETUP----##################################
HEURISTIC_WEIGHTS = { #in order of importance:
    "PieceAlmostWin": 10000, #Game-deciding MOST important!
    "PieceDangerValue": 50, #Progress (should be row^2) Get pieces to other side
    "PieceConnectDiagonal": 30, #(NEW) PROTECT PIECES
    "PieceConnectHorizontal": 40, #Make a wall
    "PieceLaneCoverage": 40, #(NEW) pieces should attack each column diagonally (offensive, leave no gaps)
    "PieceUnderAttack": -25, #Unsafe? Subtract value if under attack unless guarded
    "PieceHomeRow": 10,  #Safe against rush in early game
    "ColumnHole": -10, #Gap in defence
    "PieceConnectVertical": -20 #No protection
}
#---------------helpers--------------------
def get_my_pieces(state, player):
    # return list of players pieces in [(row, col), (row, col)] format
    grid = state["board"]
    my_pieces = [] #list of tuples
    for r in range(8):
        for c in range(8):
            if grid[r][c] == player:  # my piece
                my_pieces.append((r, c))
    return my_pieces

def get_diagonals(piece):
    #get 4 diagonals (if all valid, invalid ones not returned)
    diag = [] #list of tuple coordinate pairs (row, col)
    for i in [-1, 1]:
        for j in [-1, 1]:
            if 0 <= (piece[0] + i) < 8 and 0 <= (piece[1] + j) < 8:
                diag.append((piece[0] + i, piece[1] + j))
    return diag

def is_under_attack_by_and_is_guarded_by(state, piece, player, diags):
    #given diagonal squares to this piece:
    # is it under attack? (a piece of opposite color is diagonally "in front" of it)
    # is it guarded? (a piece of same color is "behind" it)
    is_under_attack = False
    is_guarded = False
    grid = state["board"]
    for diag in diags:
        if player == "BLACK":
            #check for white on NEXT row (under attack?)
            if diag[0] > piece[0] and grid[diag[0]][diag[1]] == "WHITE":
                is_under_attack = True
            # check for BLACK on PREVIOUS row (is guarded?)
            if diag[0] < piece[0] and grid[diag[0]][diag[1]] == "BLACK":
                is_guarded = True
        elif player == "WHITE":
            #check for black on PREVIOUS (under attack?)
            if diag[0] < piece[0] and grid[diag[0]][diag[1]] == "BLACK":
                is_under_attack = True
            # check for WHITE on NEXT row (is guarded?)
            if diag[0] > piece[0] and grid[diag[0]][diag[1]] == "WHITE":
                is_guarded = True
    return is_under_attack, is_guarded


#--------------Features---------------
def calc_almost_win(state, player, my_pieces):
    # About to win? Don't need to check if being attacked b/c its our turn
    grid = state["board"]
    score = 0
    row = 6 if player == "BLACK" else 1
    almost_goal_row = grid[row]
    for col in range(len(almost_goal_row)):
        if almost_goal_row[col] == player: #our piece almost at the goal
            # diagonals = get_diagonals((row, col)) #get valid diagonals
            # is_under_attack, is_guarded = is_under_attack_by_and_is_guarded_by(state, (row, col), player, diagonals)
            # if not is_under_attack:  # if not under attack (we want this)
            score += 1 #its our turn so we win
    return score

def calc_danger_value(state, player, my_pieces): #Progress (should be row^2 - farther is better)
    # Progress (should be row^2) Get pieces to other side! But don't just bring 1 piece out!
    score = 0
    for piece in my_pieces:
        dist = piece[0] if player == "BLACK" else (7 - piece[0])
        score += dist**2 #exponential increase for farther pieces

        diagonals = get_diagonals(piece)
        is_under_attack, is_guarded = is_under_attack_by_and_is_guarded_by(state, piece, player, diagonals)
        if not is_guarded:
            score = score * 0.5 #PENALIZE for leading 1 piece out into the open
    return score

def calc_diagonal_conn(state, player, my_pieces):
    #(NEW) PROTECT your PIECES in a chain
    # return sum of number of pieces with at least 1 piece diagonal to it
    grid = state["board"]
    score = 0
    for piece in my_pieces:
        # check piece on each of 4 diagonals to see if our color
        for diagonal in get_diagonals(piece): # get 4 tuples of coords of diagonals
            if grid[diagonal[0]][diagonal[1]] == player:
                score += 1
    return score  # sum of number of pieces with at least 1 piece diagonal to it

def calc_horizontal_conn(state, player, my_pieces):
    # Make a wall with horizontal pieces together!
    grid = state["board"]
    score = 0
    for piece in my_pieces:
        # check piece on left and right to see if our color
        if (piece[1] != 7 and grid[piece[0]][piece[1] + 1] == player) or (
                piece[1] != 0 and grid[piece[0]][piece[1] - 1] == player):
            score += 1
    return score  # sum of number of pieces next to each other horizontally

def calc_lane_coverage(state, player, my_pieces):
    #(NEW) do we have at least one piece threatening each column?
    covered_cols = [0] * 8
    for piece in my_pieces:
        diagonals = get_diagonals(piece)
        for diagonal in diagonals:
            if (player == "WHITE" and diagonal[0] < piece[0]) or (
                    player == "BLACK" and diagonal[0] > piece[0]):
                covered_cols[diagonal[1]] = 1
    return sum(covered_cols)

def calc_under_attack(state, player, my_pieces):
    # Unsafe? Subtract value if under attack unless guarded
    score = 0
    for piece in my_pieces:
        # get 4 tuples of coords of diagonals
        diagonals = get_diagonals(piece)
        is_under_attack, is_guarded = is_under_attack_by_and_is_guarded_by(state, piece, player, diagonals)
        if is_under_attack and not is_guarded: #if under attack and not guarded
            score += 1
    return score # sum of number of pieces without diagonal guards also being attacked

def calc_home_row(state, player, my_pieces): #in starting row? low points
    #Can keep pieces in home row to be safe against rush in early game
    score = 0
    home_row = state["board"][0] if player == "BLACK" else state["board"][7]
    for piece in home_row:
        if piece == player:
            score += 1
    return score

def calc_column_holes(state, player, my_pieces): #bad for us to have it
    # Do we have a gap in our defense?
    #TODO take advantage of opponent with open column?
    each_col = [0] * 8  #array of eight 0s to track which columns our pieces in
    for piece in my_pieces:
        each_col[piece[1]] += 1
    return sum(val for val in each_col if val == 0) #number of empty columns

def calc_vertical_conn(state, player, my_pieces):
    #how many pieces are DIRECTLY in front/behind of each other? (Bad for protecting)
    grid = state["board"]
    score = 0
    for piece in my_pieces:
        #check piece in front and behind to see if our color
        if (piece[0] != 7 and grid[piece[0] + 1][piece[1]] == player) or (
                piece[0] != 0 and grid[piece[0] - 1][piece[1]] == player):
            score += 1
    return score #sum of number of pieces next to each other vertically

feature_functions = {
        "PieceAlmostWin": calc_almost_win,
        "PieceDangerValue": calc_danger_value,
        "PieceConnectDiagonal": calc_diagonal_conn,
        "PieceConnectHorizontal": calc_horizontal_conn,
        "PieceLaneCoverage": calc_lane_coverage,
        "PieceUnderAttack": calc_under_attack,
        "PieceHomeRow": calc_home_row,
        "ColumnHole": calc_column_holes,
        "PieceConnectVertical": calc_vertical_conn
    }
#################################################


def defensive_eval_2(state, player):
    score = 0
    my_pieces = get_my_pieces(state, player)
    for feature, weight in HEURISTIC_WEIGHTS.items():
        func = feature_functions[feature] #get each function from the dictionary
        score += func(state, player, my_pieces) * weight
    score += random.random()  # for ties
    return score

def offensive_eval_2(state, player):
    #similar to  defensive_eval_2 but looks at opponent position
    score = 0 #my score
    opp_score = 0 #opponent score

    my_pieces = get_my_pieces(state, player)
    opponent = "WHITE" if player == "BLACK" else "BLACK"
    opp_pieces = get_my_pieces(state, opponent)

    for feature, weight in HEURISTIC_WEIGHTS.items():
        func = feature_functions[feature]  # get each function from the dictionary
        score += func(state, player, my_pieces) * weight
        opp_score += func(state, opponent, opp_pieces) * weight

    return (score - opp_score) + random.random()  #for ties

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
        'final_state': state,
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
