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
        player = state['to_move']
        board = state['board']
        legal_actions = []

        # Direction and opponent identification
        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                nr = r + direction
                if not (0 <= nr < 8):
                    continue

                # 1. Forward move: MUST be EMPTY
                if board[nr][c] == "EMPTY":
                    legal_actions.append({"from": (r, c), "to": (nr, c)})

                # 2. Diagonal-left: MUST be OPPONENT (Capture)
                if c - 1 >= 0 and board[nr][c - 1] == opponent:
                    legal_actions.append({"from": (r, c), "to": (nr, c - 1)})

                # 3. Diagonal-right: MUST be OPPONENT (Capture)
                if c + 1 < 8 and board[nr][c + 1] == opponent:
                    legal_actions.append({"from": (r, c), "to": (nr, c + 1)})

        return legal_actions

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
        new_board = deepcopy(state['board'])
        new_captures = deepcopy(state['captures'])
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        f_r, f_c = action['from']
        t_r, t_c = action['to']

        # Check for capture
        if new_board[t_r][t_c] == opponent:
            new_captures[player] += 1

        # Move piece
        new_board[t_r][t_c] = player
        new_board[f_r][f_c] = "EMPTY"

        return {
            'to_move': opponent,
            'captures': new_captures,
            'board': new_board
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
        board = state['board']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Check if White has won
        white_won = any(board[0][c] == "WHITE" for c in range(8)) or \
                    not any("BLACK" in row for row in board)

        # Check if Black has won
        black_won = any(board[7][c] == "BLACK" for c in range(8)) or \
                    not any("WHITE" in row for row in board)

        if player == "WHITE":
            if white_won: return 1
            if black_won: return -1
        else:
            if black_won: return 1
            if white_won: return -1
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
        # Check if White reached row 0 or Black reached row 7
        if any(board[0][c] == "WHITE" for c in range(8)): return True
        if any(board[7][c] == "BLACK" for c in range(8)): return True

        # Check if either side has lost all pieces
        white_exists = any("WHITE" in row for row in board)
        black_exists = any("BLACK" in row for row in board)

        return not white_exists or not black_exists


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
    """Higher value for more own pieces remaining."""
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    own_pieces = sum(row.count(player) for row in state['board'])
    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    """Higher value for fewer opponent pieces remaining."""
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_pieces = sum(row.count(opponent) for row in state['board'])
    return 2 * (16 - opp_pieces) + random.random()


def defensive_eval_2(state, player):
    """
        Beat Offensive 1: Prioritize piece count BUT add a penalty for distance to home edge.
        This encourages pieces to stay back and form a defensive line.
        """
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    board = state['board']
    own_pieces = 0
    distance_penalty = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1
                # Penalty for being too far forward
                dist_from_home = abs(r - (7 if player == "WHITE" else 0))
                distance_penalty += dist_from_home
    return (4 * own_pieces) - (0.5 * distance_penalty) + random.random()


def offensive_eval_2(state, player):
    """
        Beat Defensive 1: Prioritize advancing pieces to the goal row.
        """
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    score = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                # WHITE goal is row 0: progress = 7 - r (max at row 0)
                # BLACK goal is row 7: progress = r (max at row 7)
                progress = (7 - r) if player == "WHITE" else r
                score += (progress ** 2)  # Exponentially reward progress

            if board[r][c] == opponent:
                score -= 10  # Minor penalty for opponent pieces

    return score + random.random()

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
        'final_board': state['board']
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = MinimaxAgent("Minimax Off1", depth=2, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
