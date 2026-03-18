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
    ### Return the player to move in this state. Possible values: "WHITE" or "BLACK".
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
        board = state['board']
        player = state['to_move']

        opponent = 'BLACK' if player == 'WHITE' else 'WHITE'

        direction = -1 if player == 'WHITE' else 1
        legal_moves = []

        for row in range(8):
            for col in range(8):
                if board[row][col] == player:
                    nr = row + direction

                    if 0 <= nr < 8:
                        # move forward
                        if board[nr][col] == "EMPTY":
                            legal_moves.append({"from": (row, col), "to": (nr, col)})

                        # move diagonal left and capture
                        if col - 1 >= 0 and board[nr][col - 1] == opponent:
                            legal_moves.append({"from": (row, col), "to": (nr, col - 1)})

                        # move diagonal right and capture
                        if col + 1 < 8 and board[nr][col + 1] == opponent:
                            legal_moves.append({"from": (row, col), "to": (nr, col + 1)})

        return legal_moves


    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).

        updated_state = deepcopy(state)
        board = updated_state['board']
        player = state['to_move']

        opponent = 'BLACK' if player == 'WHITE' else 'WHITE'

        if action is None:
            print("Action is None. Returning state unchanged.")
            return state

        (row1, col1) = action['from']
        (row2, col2) = action['to']

        if board[row2][col2] == opponent:
            updated_state['captures'][player] += 1

        board[row2][col2] = player
        board[row1][col1] = 'EMPTY'

        updated_state['to_move'] = opponent

        return updated_state




    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

        if not self.terminal_test(state):
            return 0

        win = 'BLACK' if state['to_move'] == "WHITE" else 'WHITE'

        if win == player:
            return 1
        else:
            return -1



    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]

        # white terminates
        if any(board[0][col] == "WHITE" for col in range(8)):
            return True

        # black terminates
        if any(board[7][col] == "BLACK" for col in range(8)):
            return True

        # no more pieces
        white = sum(row.count("WHITE") for row in board)
        black = sum(row.count("BLACK") for row in board)

        if white == 0 or black == 0:
            return True

        return False


    def display(self, state):
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print("\n".join("".join(chars[state['board'][row][col]] for col in range(8)) for row in range(8)))
        if self.terminal_test(state):
            if self.to_move(state) == "WHITE":
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {state['to_move']}")
        print(f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")



##########################################################################
# code here
# Evaluation functions

def count_pieces(state, player):
    return sum(row.count(player) for row in state["board"])

def opponent_of(player):
    return "BLACK" if player == "WHITE" else "WHITE"


def defensive_eval_1(state, player):
    own = count_pieces(state, player)
    return 2 * own + random.random()


def offensive_eval_1(state, player):
    opponent = opponent_of(player)
    opp = count_pieces(state, opponent)
    return 2 * (32 - opp) + random.random()


def defensive_eval_2(state, player):
    opponent = opponent_of(player)

    own = count_pieces(state, player)
    opp = count_pieces(state, opponent)

    material = 5 * (own - opp)

    advancement = 0
    for row in range(8):
        for col in range(8):
            if state["board"][row][col] == player:
                advancement += (7 - row) if player == "WHITE" else row

    captures = 10 * state["captures"][player]

    almost_win = 0
    target_row = 1 if player == "WHITE" else 6
    for col in range(8):
        if state["board"][target_row][col] == player:
            almost_win += 15

    return material + 0.5 * advancement + captures + almost_win


def offensive_eval_2(state, player):
    opponent = opponent_of(player)

    own = count_pieces(state, player)
    opp = count_pieces(state, opponent)

    material = 6 * (own - opp)

    home_row = 7 if player == "WHITE" else 0
    home_defense = sum(3 for c in range(8)
                       if state["board"][home_row][c] == player)

    connection = 0
    for row in range(8):
        for col in range(7):
            if state["board"][row][col] == player and state["board"][row][col + 1] == player:
                connection += 2

    opponent_advancement = 0
    for row in range(8):
        for col in range(8):
            if state["board"][row][col] == opponent:
                opponent_advancement += (7 - row) if opponent == "WHITE" else row

    return material + home_defense + connection - 0.4 * opponent_advancement

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
        "final_state": {
            "board": deepcopy(state["board"])
        }
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
