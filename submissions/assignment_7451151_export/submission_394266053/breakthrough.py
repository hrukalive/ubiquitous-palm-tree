import random
from copy import deepcopy
from distutils.command.install import value

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):

    WHITE = "WHITE"
    BLACK = "BLACK"
    EMPTY = "EMPTY"
    GRID_SIZE = 8

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
        actions = []
        board = state['board']
        player = self.to_move(state)

        # Determine move direction and opponent
        if player == Breakthrough.WHITE:
            direction = -1  # White moves up
            opponent = Breakthrough.BLACK
        else:
            direction = 1  # Black moves down
            opponent = Breakthrough.WHITE

        # Iterate over all board positions
        for row in range(Breakthrough.GRID_SIZE):
            for col in range(Breakthrough.GRID_SIZE):
                if board[row][col] != player:
                    continue  # Skip empty or opponent squares

                next_row = row + direction
                if not (0 <= next_row < Breakthrough.GRID_SIZE):
                    continue  # Cannot move off the board

                # --- Forward move ---
                if board[next_row][col] == Breakthrough.EMPTY:
                    actions.append({"from": (row, col), "to": (next_row, col)})

                # --- Diagonal left capture ---
                if col - 1 >= 0 and (board[next_row][col - 1] == opponent or board[next_row][col - 1] == Breakthrough.EMPTY):
                    actions.append({"from": (row, col), "to": (next_row, col - 1)})

                # --- Diagonal right capture ---
                if col + 1 < Breakthrough.GRID_SIZE and (board[next_row][col + 1] == opponent or board[next_row][col + 1] == Breakthrough.EMPTY):
                    actions.append({"from": (row, col), "to": (next_row, col + 1)})


        return actions
        raise NotImplementedError

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

        player = self.to_move(state)
        opponent = ""
        if player == Breakthrough.WHITE:
            opponent = Breakthrough.BLACK
        else:
            opponent = Breakthrough.WHITE

        r, c = action['from']
        nr, nc = action['to']

        #Check capture
        if new_board[nr][nc] == opponent:
            new_captures[player] += 1

        new_board[nr][nc] = player
        new_board[r][c] = Breakthrough.EMPTY

        return {
            'to_move': opponent,  # Player is also a string "WHITE" or "BLACK".
            'captures': new_captures,  # Initially, white and black have captured 0 pieces.
            'board': new_board,  # 8x8 grid representing the board.
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
        if not self.terminal_test(state):
            return 0

        board = state['board']

        for col in range(Breakthrough.GRID_SIZE):
            if board[0][col] == Breakthrough.WHITE:
                winner = Breakthrough.WHITE
                return 1 if player == winner else -1

            if board[Breakthrough.GRID_SIZE - 1][col] == Breakthrough.BLACK:
                winner = Breakthrough.BLACK
                return 1 if player == winner else -1

            # If terminal and no breakthrough,
            # then it must be no legal moves → current player loses
        loser = state['to_move']
        winner = Breakthrough.BLACK if loser == Breakthrough.WHITE else Breakthrough.WHITE

        return 1 if player == winner else -1


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state['board']

        for col in range(Breakthrough.GRID_SIZE):
            if board[0][col] == Breakthrough.WHITE:
                return True
            if board[Breakthrough.GRID_SIZE - 1][col] == Breakthrough.BLACK:
                return True

        #If player has no legal moves
        if len(self.actions(state)) == 0:
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

   board = state['board']
   own_pieces = 0
   for row in range(Breakthrough.GRID_SIZE):
       for col in range(Breakthrough.GRID_SIZE):

           if board[row][col] == player:
               own_pieces += 1

   value = 2 * own_pieces + random.random()
   return value


def offensive_eval_1(state, player):

    board = state['board']
    opponent_pieces = 0
    opponent = ""
    if player == Breakthrough.WHITE:
        opponent = Breakthrough.BLACK
    else:
        opponent = Breakthrough.BLACK

    for row in range(Breakthrough.GRID_SIZE):
        for col in range(Breakthrough.GRID_SIZE):

            if board[row][col] == opponent:
                opponent_pieces += 1

    value = 2*(32 - opponent_pieces) + random.random()
    return value


def defensive_eval_2(state, player):
    MATERIAL_WEIGHT = 8  # Stronger than offensive eval
    SUPPORT_BONUS = 2
    BEHIND_BONUS = 3
    ISOLATION_PENALTY = -4
    ADVANCE_WEIGHT = 0.3  # Small positional bonus

    board = state['board']
    score = 0

    for row in range(Breakthrough.GRID_SIZE):
        for col in range(Breakthrough.GRID_SIZE):
            piece = board[row][col]

            if piece == Breakthrough.WHITE:
                support = 0

                # Check supporting pieces behind
                if row + 1 < Breakthrough.GRID_SIZE:
                    if board[row + 1][col] == Breakthrough.WHITE:
                        support += BEHIND_BONUS
                    if col - 1 >= 0 and board[row + 1][col - 1] == Breakthrough.WHITE:
                        support += SUPPORT_BONUS
                    if col + 1 < Breakthrough.GRID_SIZE and board[row + 1][col + 1] == Breakthrough.WHITE:
                        support += SUPPORT_BONUS

                if support == 0:
                    support = ISOLATION_PENALTY

                # Small advancement bonus
                advance_score = (Breakthrough.GRID_SIZE - 1 - row) * ADVANCE_WEIGHT

                score += support + advance_score

            elif piece == Breakthrough.BLACK:
                support = 0

                if row - 1 >= 0:
                    if board[row - 1][col] == Breakthrough.BLACK:
                        support += BEHIND_BONUS
                    if col - 1 >= 0 and board[row - 1][col - 1] == Breakthrough.BLACK:
                        support += SUPPORT_BONUS
                    if col + 1 < Breakthrough.GRID_SIZE and board[row - 1][col + 1] == Breakthrough.BLACK:
                        support += SUPPORT_BONUS

                if support == 0:
                    support = ISOLATION_PENALTY

                advance_score = row * ADVANCE_WEIGHT

                score -= (support + advance_score)

    material_diff = (
            state['captures'][Breakthrough.WHITE]
            - state['captures'][Breakthrough.BLACK]
    )

    score += material_diff * MATERIAL_WEIGHT

    # Return from perspective of player
    if player == Breakthrough.WHITE:
        return score
    else:
        return -score

def offensive_eval_2(state, player):
    ROW_FACTOR = 1.2
    THREAT_BONUS = 2.5
    MOBILITY_BONUS = 0.3
    CAPTURE_WEIGHT = 4
    OPP_ADVANCE_PENALTY = 0.8

    board = state['board']
    score = 0

    for row in range(Breakthrough.GRID_SIZE):
        for col in range(Breakthrough.GRID_SIZE):
            piece = board[row][col]

            # -----------------------
            # WHITE PIECES (attacking upward)
            # -----------------------
            if piece == Breakthrough.WHITE:

                # Linear advancement
                advance = Breakthrough.GRID_SIZE - row - 1
                score += advance * ROW_FACTOR

                # Mobility (forward + diagonals if empty)
                if row + 1 < Breakthrough.GRID_SIZE:
                    # forward move
                    if board[row + 1][col] == Breakthrough.EMPTY:
                        score += MOBILITY_BONUS

                    # diagonal capture threats
                    for dc in [-1, 1]:
                        new_col = col + dc
                        if 0 <= new_col < Breakthrough.GRID_SIZE:
                            if board[row + 1][new_col] == Breakthrough.BLACK:
                                score += THREAT_BONUS

            # -----------------------
            # BLACK PIECES
            # -----------------------
            elif piece == Breakthrough.BLACK:

                # Penalize opponent advancement
                score -= row * OPP_ADVANCE_PENALTY

                # Penalize opponent threats
                if row - 1 >= 0:
                    for dc in [-1, 1]:
                        new_col = col + dc
                        if 0 <= new_col < Breakthrough.GRID_SIZE:
                            if board[row - 1][new_col] == Breakthrough.WHITE:
                                score -= THREAT_BONUS

    # Material via captures
    capture_difference = (
            state['captures'][Breakthrough.WHITE]
            - state['captures'][Breakthrough.BLACK]
    )
    score += capture_difference * CAPTURE_WEIGHT

    if player == Breakthrough.WHITE:
        return score
    else:
        return -score






    
    return ...

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
        'final_board': state['board'],
        'to_move': state['to_move'],
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
