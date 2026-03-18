import copy
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
        direction = 0
        opponent = ""
        board = state['board']
        moves = []
        player = state['to_move']
        #White starts from row 6-7
        if player == "WHITE":
            direction = -1
            opponent = "BLACK"
        #Black start from row 0-1
        elif player == "BLACK":
            direction = 1
            opponent = "WHITE"
        for r in range(8):
            for c in range(8):
                #Check if the board position contains player piece
                if board[r][c] == player:
                    #Get the next row
                    new_r = r + direction
                    #Check bounds
                    if 0 <= new_r < 8:
                        #Check if forward  is empty
                        if board[new_r][c] == "EMPTY":
                            moves.append({"from": (r, c), "to": (new_r, c)})
                        #Diagonal left
                        if c - 1 >= 0:
                            if board[new_r][c - 1] == "EMPTY" or board[new_r][c - 1] == opponent:
                                moves.append({"from": (r, c), "to": (new_r, c - 1)})
                        #Diagonal right
                        if c + 1 < 8:
                            if board[new_r][c + 1] == "EMPTY" or board[new_r][c + 1] == opponent:
                                moves.append({"from": (r, c), "to": (new_r, c + 1)})
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
        #Create deep copy so original state not modified
        new_state = deepcopy(state)
        board = new_state['board']
        player = new_state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        #Initial board position
        r1, c1 = action["from"]
        #Target board position
        r2, c2 = action["to"]
        #Captures piece if target position has opponent piece
        if board[r2][c2] == opponent:
            new_state['captures'][player] += 1
        #Update piece position
        board[r2][c2] = player
        board[r1][c1] = "EMPTY"
        #Switch turn
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
        board = state['board']
        for c in range(8):
            #If white reaches opposite end, if player is white, win, otherwise loss
            if board[0][c] == "WHITE":
                return 10000 if player == "WHITE" else -10000
            #If black reaches opposite end, if player is black, win, otherwise loss
            elif board[7][c] == "BLACK":
                return 10000 if player == "BLACK" else -10000
        #If white captures all opponents pieces win if player is white, otherwise loss
        if state['captures']["WHITE"] == 16:
            return 10000 if player == "WHITE" else -10000
        #If black captures all opponents pieces win if player is black, otherwise loss
        if state['captures']["BLACK"] == 16:
            return 10000 if player == "BLACK" else -10000
        return 0

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]
        #White reaches row 0
        for c in range(8):
            if board[0][c] == "WHITE":
                return True
        #Black reaches row 7
        for c in range(8):
            if board[7][c] == "BLACK":
                return True
        #All pieces captured
        white_exists = False
        black_exists = False
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_exists = True
                if board[r][c] == "BLACK":
                    black_exists = True
        if not white_exists or not black_exists:
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
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    #Check how many pieces have been captured to get remaining pieces
    player_pieces_left = 16 - state['captures'][opponent]
    return 2 * player_pieces_left + random.random()


def offensive_eval_1(state, player):
    #Check how many pieces have been captured to get opponent pieces
    opponent_pieces_left = 16 - state['captures'][player]
    return 2 * (32 - opponent_pieces_left) + random.random()


def defensive_eval_2(state, player):
    #Defensive evaluation function that prioritizes number of pieces and structure while capturing opponents
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    #Number of player pieces
    own_pieces = 0
    #Pieces threatened to be captured, but defended by teammates
    under_attack = 0
    #Protected diagonally
    diagonal_protected = 0
    #How many pieces on the defense home row
    home_row_pieces = 0
    #Reward some advancement
    advancement_score = 0
    #Horizontally connected
    horizontally_connected = 0
    #Vertically connected
    vertically_connected = 0
    isolated_pieces = 0
    opponent_almost_win = 0
    captured_opponent = state['captures'][player]
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1
                #Keep track of pieces under attack
                if is_under_attack(board, r, c, player):
                    under_attack += 1
                #Diagonal protection
                if is_diagonally_protected(board, r, c, player):
                    diagonal_protected += 1
                #Home row defense
                if player == "WHITE" and r == 7:
                    home_row_pieces += 1
                if player == "BLACK" and r == 0:
                    home_row_pieces += 1
                #Advancement
                if player == "WHITE":
                    advancement_score += (6 - r)
                else:
                    advancement_score += (r - 1)
                #Make sure left and right columns in bounds
                #Count connected horizontally
                if (c > 0 and board[r][c - 1] == player) or (c < 7 and board[r][c + 1] == player):
                    horizontally_connected += 1
                #Count connected vertically
                if (r > 0 and board[r - 1][c] == player) or (r < 7 and board[r + 1][c] == player):
                    vertically_connected += 1
                # Isolated pieces
                # Get coordinates around the piece, find a teammate
                isolated = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == player:
                            isolated = False
                            break
                    if not isolated:
                        break
                if (player == "WHITE" and r > 2) or (player == "BLACK" and r < 5):
                    if isolated:
                        isolated_pieces += 1
            if board[r][c] == opponent:
                # If opponent is WHITE = almost win at row 1
                if opponent == "WHITE" and r == 1:
                    opponent_almost_win += 1
                # If opponent is BLACK = almost win at row 6
                if opponent == "BLACK" and r == 6:
                    opponent_almost_win += 1
    #Linear Combinations and weights
    value = (
        8 * own_pieces #Num pieces is most important
        - 10 * opponent_almost_win #Prevent opponent from getting in winning position
        - 6 * under_attack #Prevent blunders
        - 5 * isolated_pieces #No lone pieces, easily defenseless
        + 4 * captured_opponent #Make safe captures
        + 4 * diagonal_protected #Good defensive structure
        + 2 * horizontally_connected
        + 2 * vertically_connected
        + 3 * home_row_pieces
        + 1 * advancement_score #Advance slowly
        + random.random()
    )
    return value

def offensive_eval_2(state, player):
    #Offensive evaluation function that prioritizes advancing pieces with structure
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    #Safe pieces almost at opponents end
    piece_almost_win = 0
    #Number of advanced pieces
    advancement_score = 0
    #Advance pieces in diagonal formation
    diagonal_protected = 0
    #Pieces threatened to be captured
    under_attack = 0
    own_pieces = 0
    captured_opponent = state['captures'][player]
    #Isolated pieces not close to goal
    isolated_pieces = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1
                #AdvancedScore
                #Since white starts at row 0 and 1, can advance up 6 squares
                if player == "WHITE":
                    advancement_score += (6 - r)
                #Black pieces starts at row 6 and 7, can advance down 6 squares
                else:
                    advancement_score += (r - 1)
                #PieceAlmostWin
                #White one row away from winning and not under attack
                if player == "WHITE" and r == 1:
                    if not is_under_attack(board, r, c, player):
                        piece_almost_win += 1
                #Black one row away from winning and not under attack
                if player == "BLACK" and r == 6:
                    if not is_under_attack(board, r, c, player):
                        piece_almost_win += 1
                #Keep track of pieces under attack
                if is_under_attack(board, r, c, player):
                    under_attack += 1
                #DiagonallyProtected
                if is_diagonally_protected(board, r, c, player):
                    diagonal_protected += 1
                #Check adjacent rows and columns for isolation
                # Diagonal protection
                if is_diagonally_protected(board, r, c, player):
                    diagonal_protected += 1
                # Isolated pieces
                # Get coordinates around the piece, find a teammate
                isolated = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == player:
                            isolated = False
                            break
                    if not isolated:
                        break
                if (player == "WHITE" and r > 2) or (player == "BLACK" and r < 5):
                    if isolated:
                        isolated_pieces += 1

    #Linear Combinations and weights
    value = (
            20 * piece_almost_win #Prioritize pieces close to winning
            + 5 * advancement_score #Advance pieces
            + 4 * captured_opponent #Make sure to capture as well
            + 3 * diagonal_protected #Some backup for advanced pieces
            - 6 * under_attack #Prevent pieces attacked without backup
            - 3 * isolated_pieces #Prevent isolated pieces
            + 1 * own_pieces #Keep track of pieces owned
            + random.random()
    )

    return value

#Helper function for if a piece is under attack
def is_under_attack(board, r, c, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    if player == "WHITE":
        #Since white going down the grid, attack row is one below
        attack_row = r - 1
        #Make sure it's in bounds
        if attack_row >= 0:
            #Under attack from left
            if c - 1 >= 0 and board[attack_row][c - 1] == opponent:
                return True
            if c + 1 < 8 and board[attack_row][c + 1] == opponent:
                return True
    #Black
    else:
        #Since black going up the grid, attack row is one above
        attack_row = r + 1
        if attack_row < 8:
            #Under attack from left
            if c - 1 >= 0 and board[attack_row][c - 1] == opponent:
                return True
            #Under attack from right
            if c + 1 < 8 and board[attack_row][c + 1] == opponent:
                return True

    return False

#Helper function for diagonally protected pieces
def is_diagonally_protected(board, r, c, player):
    if player == "WHITE":
        #Next row of a piece protects the piece
        protect_row = r + 1
        if protect_row < 8:
            #Check if piece is protected left diagonally
            if c - 1 >= 0 and board[protect_row][c - 1] == player:
                return True
            #Check if piece is protected right diagonally
            if c + 1 < 8 and board[protect_row][c + 1] == player:
                return True
    #Black is opposite
    else:
        #Previous row of a piece protects the piece
        protect_row = r - 1
        if protect_row >= 0:
            #Check if piece is protected left diagonally
            if c - 1 >= 0 and board[protect_row][c - 1] == player:
                return True
            #Check if piece is protected right diagonally
            if c + 1 < 8 and board[protect_row][c + 1] == player:
                return True

    return False

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
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
