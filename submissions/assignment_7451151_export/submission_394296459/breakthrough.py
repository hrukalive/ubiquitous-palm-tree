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
            'board': grid                         # 8x8 grid representing the board.
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

    def get_pieces(self, state, player):
        player_pieces = []
        for x, row in enumerate(state['board']):
            for y, piece in enumerate(row):
                if piece == player:
                    player_pieces.append([x, y])
        return player_pieces

    def get_moves(self, piece, state):
        moves = []
        row_mov = 0
        opp = ""
        if state['to_move'] == "WHITE":
            row_mov = -1
            opp = "BLACK"
        elif state['to_move'] == "BLACK":
            row_mov = 1
            opp = "WHITE"
        movement = [(row_mov, -1), (row_mov, 0), (row_mov, 1)]
        for move in movement:
            target = (piece[0] + move[0], piece[1] + move[1])
            if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                board_tg = state['board'][target[0]][target[1]]
                if  board_tg == "EMPTY":
                    moves.append({
                        "from" : tuple(piece),
                        "to" : target
                    })
                elif board_tg == opp and not move[1] == 0:
                    moves.append({
                        "from": tuple(piece),
                        "to": target
                    })
        return moves

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
        player = self.to_move(state)
        pieces = self.get_pieces(state, player)
        moves = []
        for piece in pieces:
            p_moves = self.get_moves(piece, state)
            moves = moves + p_moves
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

        # Get the player
        player = self.to_move(state)
        # Get the opponent
        if player == "WHITE":
            opp = "BLACK"
        else:
            opp = "WHITE"
        # Get board (deepcopy to avoid modifying original state)
        board = deepcopy(state['board'])
        # Get captures
        captures = deepcopy(state['captures'])

        # Get initial and target coordinates
        initial_row, initial_col = action["from"]
        target_row, target_col = action["to"]

        # Get what's on the target square currently
        target = board[target_row][target_col]

        # If the target is the opponent, captures of the player go up.
        if target == opp:
            captures[player] += 1

        # Perform move
        board[initial_row][initial_col] = "EMPTY"
        board[target_row][target_col] = player

        return {
            'to_move' : opp,
            'captures' : captures,
            'board' : board
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
        if self.terminal_test(state):
            return -1000 if state['to_move'] == player else 1000
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
        captures = state['captures']
        # If there have been 16 captures from one player
        if captures['WHITE'] == 16 or captures['BLACK'] == 16:
            return True

        # If any player reached the other side of the board
        if "WHITE" in board[0] or "BLACK" in board[7]:
            return True

        # Else return false
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
    if player == "WHITE":
        opp = "BLACK"
    else:
        opp = "WHITE"
    num_pieces_player = 16 - state['captures'][opp]
    return 2 * num_pieces_player + random.random()


def offensive_eval_1(state, player):
    opp_pieces = 16 - state['captures'][player]
    return 2 * (32 - opp_pieces) + random.random()

# Returns 500 if an unguarded piece is about to reach the end of the board,
# or if there's two or more guarded pieces on the second line before the end of the board
def piece_almost_win(state, player, opp):
    count = 0
    board = state['board']
    if player == "WHITE":
        row = 6
        forward = 1
    else:
        row = 1
        forward = -1
    base_row = board[row]
    for x, square in enumerate(base_row):
        if square == opp:
            if count == 0:
                if x == 0:
                    if not board[row + forward][x + 1] == player:
                        return -500
                elif x == 7:
                    if not board[row + forward][x - 1] == player:
                        return -500
                else:
                    if not board[row + forward][x - 1] == player and not board[row + forward][x + 1] == player:
                        return -500
                count += 1
            if count > 0:
                return -500
    return 0


def defense_line_value(state, player):
    value = 0
    contig_empty = 0
    board = state['board']
    if player == "BLACK":
        rows = (0, 1)
    else:
        rows = (7, 6)
    for piece in board[rows[0]]:
        if piece == player:
            value -= contig_empty
            contig_empty = 0
            value += 6 * random.random()
        else:
            contig_empty += 2
    for piece in board[rows[1]]:
        if piece == player:
            value -= contig_empty
            contig_empty = 0
            value += 3 * random.random()
        else:
            contig_empty += 1
    return value

def attack_line_value(state, player):
    value = 0
    contig_empty = 0
    board = state['board']
    if player == "BLACK":
        rows = (6, 5)
    else:
        rows = (1, 2)
    for piece in board[rows[0]]:
        if piece == player:
            value -= contig_empty
            contig_empty = 0
            value += 6 * random.random()
        else:
            contig_empty += 2
    for piece in board[rows[1]]:
        if piece == player:
            value -= contig_empty
            contig_empty = 0
            value += 3 * random.random()
        else:
            contig_empty += 1
    return value

def position_value(state, player, opp):
    board = state['board']
    if player == "WHITE":
        end_row = 0
    else:
        end_row = 7
    value = 0
    for x, row in enumerate(board):
        for piece in row:
            if piece == player:
                value += (8 - abs(end_row - x)) * random.random()
    return value

# Returns 10* number of player pieces that have a free path towards the opp base
def unstoppable_piece(state, player, opp):
    board = state['board']
    value = 0
    if player == "WHITE":
        row = 0
        forward = 1
    else:
        row = 7
        forward = -1
    for i in range(4):
        theRow = row + forward*i
        for x, piece in enumerate(board[theRow]):
            if piece == player:
                val = 10
                for r in range(theRow, row):
                    for c in range(x -1,x + 1):
                        if c > 0 and c < 7:
                            if board[r][c] == opp:
                                val = 0
                value += val
    return value

def defensive_eval_2(state, player):
    value = 0
    if player == "WHITE":
        opp = "BLACK"
    else:
        opp = "WHITE"
    captures_opp = state['captures'][opp]
    value += 4 * (16-captures_opp) * random.random()
    value += defense_line_value(state, player)
    value += piece_almost_win(state, player, opp)

    return value


def offensive_eval_2(state, player):
    value = 0
    if player == "WHITE":
        opp = "BLACK"
    else:
        opp = "WHITE"
    captures = state['captures'][player]
    value += 4 * captures * random.random()
    value -= piece_almost_win(state, opp, player)
    value += attack_line_value(state, player)
    value += position_value(state, player, opp)
    value += unstoppable_piece(state, player, opp)

    return value

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
        'final_board': deepcopy(state['board'])
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = MinimaxAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=offensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, progress=True)
    print(results)
