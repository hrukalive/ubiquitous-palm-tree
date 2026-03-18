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
        for row in range(0, 2):
            for column in range(8):
                grid[row][column] = "BLACK"
        for row in range(6, 8):
            for column in range(8):
                grid[row][column] = "WHITE"
        return {
            'to_move': "WHITE",                   # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0}, # Initially, white and black have captured 0 pieces.
            'board': grid,                        # 8x8 grid representing the board.
        } # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):
        return state['to_move']
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

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

        board = state['board']
        player = state['to_move']
        row_change = -1 if player == 'WHITE' else 1

        moves = []
        for row in range(8):
            for column in range(8):
                if board[row][column] != player:
                    continue
                next_row = row + row_change
                if not (0 <= next_row < 8):
                    continue

                #straight forward only if empty
                if board[next_row][column] == "EMPTY":
                    moves.append({"from": (row, column), "to": (next_row, column)})

                #left diagonal
                if column-1 >= 0 and board[next_row][column-1] != player:
                    moves.append({"from": (row, column), "to": (next_row, column-1)})

                #right diagonal
                if column+1 < 8 and board[next_row][column+1] != player:
                    moves.append({"from": (row, column), "to": (next_row, column+1)})

        return moves



    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).

        board = [row[:] for row in state['board']]
        captures = dict(state['captures'])
        player = state['to_move']
        opponent = "BLACK" if player == 'WHITE' else "WHITE"

        past_row, past_column = action["from"]
        to_row, to_column = action["to"]

        if board[to_row][to_column] == opponent:
            captures[player] += 1

        board[to_row][to_column] = player
        board[past_row][past_column] = "EMPTY"

        return{
            'to_move': opponent,
            'captures': captures,
            'board': board,
        }


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        board = state['board']
        opponent = "BLACK" if player == 'WHITE' else "WHITE"

        #check wins
        if player == "WHITE" and any(board[0][column] == "WHITE" for column in range(8)):
            return 1
        if player == "BLACK" and any(board[7][column] == "BLACK" for column in range(8)):
            return 1
        if opponent == "WHITE" and any(board[0][column] == "WHITE" for column in range(8)):
            return -1
        if opponent == "BLACK" and any (board[7][column] == "BLACK" for column in range(8)):
            return -1

        white_on_board = any(board[row][column] == "WHITE" for row in range(8) for column in range(8))
        black_on_board = any(board[row][column] == "BLACK" for row in range(8) for column in range(8))

        if not white_on_board:
            return 1 if player == "BLACK" else -1
        if not black_on_board:
            return 1 if player == "WHITE" else -1

        return 0

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state['board']

        #White reaches back row and wins
        if any(board[0][column] == "WHITE" for column in range(8)):
            return True

        #Black reaches back row and wins
        if any(board[7][column] == "BLACK" for column in range(8)):
            return True

        #All pices of either player eliminated
        white_on_board = any(board[row][column] == "WHITE" for row in range(8) for column in range(8))
        black_on_board = any(board[row][column] == "BLACK" for row in range(8) for column in range(8))

        return not white_on_board or not black_on_board


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
    #given defensive eval return
    board = state['board']
    number_of_own_pieces_remaining = sum(board[row][column] == player for row in range(8) for column in range(8))
    return 2 * (number_of_own_pieces_remaining) + random.random()


def offensive_eval_1(state, player):
    #given offensive eval return
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    number_of_opponent_pieces_remaining  = sum(board[row][column] == opponent for row in range(8) for column in range(8))
    return 2 * (32 - number_of_opponent_pieces_remaining) + random.random()


def defensive_eval_2(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    #counters
    own_pieces = 0
    horizontal_pairs = 0
    threat = 0.0
    column_has_defense = [False] * 8

    #loop
    for row in range(8):
        for column in range(8):
            cell = board[row][column]
            if cell == player:
                own_pieces += 1
                column_has_defense[column] = True

                #checking for pair defense
                if column + 1 < 8 and board[row][column + 1] == player:
                    horizontal_pairs += 1

            elif cell == opponent:
                #under attack, dangerous
                if player == "WHITE":
                    threat += row / 7.0 #black pieces near row 7 are highest danger

                else:
                    threat += (7 - row) / 7.0 #white pieces near row 0 are most dangerous

    #checking for column gaps
    column_gaps = sum(1 for has_piece in column_has_defense if not has_piece)
    
    return 2 * own_pieces + 3 * horizontal_pairs - 4 * column_gaps - 8 * threat + random.random()


def offensive_eval_2(state, player):
    board = state['board']

    #count of piece value and the num pieces close to winning
    advanced_pieces = 0
    own_pieces = 0

    #scan every cell on the board skipping spots without player
    for row in range(8):
        for column in range(8):
            if board[row][column] != player:
                continue
            own_pieces += 1
            #how far the piece has gone over the midpoint
            if player == "WHITE":
                advanced_pieces += 7 - row
            else:
                advanced_pieces += row

    #almost winning pieces heavily prioritized with some points for keeping pieces
    return 2 * own_pieces + 3 * advanced_pieces + random.random()



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
