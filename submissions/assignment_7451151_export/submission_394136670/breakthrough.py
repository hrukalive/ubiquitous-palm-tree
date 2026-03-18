import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.


class Breakthrough(Game):
    def initial_state(self):  # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.

        # Make an 8x8 grid where every square starts out empty
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]

        # Fill the top two rows (rows 0 and 1) with BLACK pieces
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"

        # Fill the bottom two rows (rows 6 and 7) with WHITE pieces
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"

        return {
            "to_move": "WHITE",                    # Player is also a string "WHITE" or "BLACK".
            "captures": {"WHITE": 0, "BLACK": 0},  # Initially, white and black have captured 0 pieces.
            "board": grid,                         # 8x8 grid representing the board.
        }  # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

        # The state dictionary already stores whose turn it is, so just return it
        return state["to_move"]

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

        board = state["board"]
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # WHITE moves up the board (row numbers get smaller)
        # BLACK moves down the board (row numbers get bigger)
        direction = -1 if player == "WHITE" else 1

        moves = []  # We'll collect every legal move into this list

        # Check every square on the board
        for r in range(8):
            for c in range(8):

                # Skip this square if it doesn't have one of our pieces
                if board[r][c] != player:
                    continue

                # The square directly in front of this piece
                nr = r + direction

                # If moving forward would go off the board, skip this piece
                if not (0 <= nr < 8):
                    continue

                # A piece can move straight forward ONLY if that square is empty
                # (pieces cannot capture by going straight ahead)
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})

                # A piece can move diagonally forward (left or right) if:
                #   - the diagonal square is empty, OR
                #   - the diagonal square has an enemy piece (capture!)
                for dc in [-1, 1]:  # dc = -1 is left diagonal, dc = +1 is right diagonal
                    nc = c + dc     # column of the diagonal square

                    # Make sure the diagonal square is on the board and not one of our own pieces
                    if 0 <= nc < 8 and board[nr][nc] != player:
                        moves.append({"from": (r, c), "to": (nr, nc)})

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

        # Make a full copy of the board so we don't accidentally change the original state
        board = deepcopy(state["board"])

        # Copy the capture counts so we can update them without touching the original
        captures = {"WHITE": state["captures"]["WHITE"], "BLACK": state["captures"]["BLACK"]}

        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Unpack the starting square and the destination square from the action
        fr, fc = action["from"]  # "from" row and column
        tr, tc = action["to"]    # "to" row and column

        # If an enemy piece is sitting on the destination square, we captured it
        if board[tr][tc] == opponent:
            captures[player] += 1

        # Place our piece on the destination square and clear the square we came from
        board[tr][tc] = player
        board[fr][fc] = "EMPTY"

        # It is now the other player's turn
        next_player = "BLACK" if player == "WHITE" else "WHITE"

        return {
            "to_move": next_player,
            "captures": captures,
            "board": board,
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

        # This function is only called when the game is already over.
        # Whoever's turn it is to move RIGHT NOW is actually the loser —
        # because the other player just made the winning move on the previous turn.
        winner = "BLACK" if state["to_move"] == "WHITE" else "WHITE"

        # Return +1 if the player we're evaluating for won, -1 if they lost
        return 1 if winner == player else -1

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        # The game ends when:
        # (a) A WHITE piece reaches row 0 (BLACK's home row), or
        # (b) A BLACK piece reaches row 7 (WHITE's home row), or
        # (c) All pieces of one player are captured.

        board = state["board"]
        white_count = 0
        black_count = 0

        # Check the top row for a WHITE piece — that means WHITE made it across
        # Check the bottom row for a BLACK piece — that means BLACK made it across
        for c in range(8):
            if board[0][c] == "WHITE":
                return True
            if board[7][c] == "BLACK":
                return True

        # Count how many pieces each player still has on the board
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_count += 1
                elif board[r][c] == "BLACK":
                    black_count += 1

        # If one side has zero pieces left, the game is over
        return white_count == 0 or black_count == 0

    def display(self, state):
        # Use single letters so the board fits neatly in the terminal
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print("\n".join("".join(chars[state["board"][r][c]] for c in range(8)) for r in range(8)))
        if self.terminal_test(state):
            # The player who is "to_move" right now actually lost on the previous move
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
    """
    Defensive Evaluation 1: The more pieces you have remaining, the higher your value is.
    Formula: 2 * (number_of_own_pieces_remaining) + random()
    """
    board = state["board"]

    # Count how many of our own pieces are still alive on the board
    own_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)

    # Multiply by 2 and add a tiny random number to break ties
    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    """
    Offensive Evaluation 1: The more pieces opponent has remaining, the lower your value is.
    Formula: 2 * (32 - number_of_opponent_pieces_remaining) + random()
    """
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state["board"]

    # Count how many enemy pieces are still on the board
    opp_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent)

    # The game starts with 32 total pieces (16 per side).
    # Fewer enemy pieces means a better score for us.
    return 2 * (32 - opp_pieces) + random.random()


def defensive_eval_2(state, player):
    """
    Defensive Evaluation 2: A smarter defensive score designed to beat Offensive Eval 1.

    Instead of just counting our pieces, we look at several things at once:
    - How many of our pieces are still alive (more = better)
    - How far enemy pieces have advanced into our side of the board (more = worse for us)
    - How many of our pieces are about to be captured (more = worse)
    - How many of our pieces are sitting next to a friendly piece horizontally (more = better,
      because side-by-side pieces protect each other)
    - How many of our pieces are still on our home row (more = better, last line of defense)

    We multiply each factor by a weight and add them all up.
    """
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # Figure out which direction the opponent moves so we can tell if they threaten us
    # WHITE moves up (direction -1), BLACK moves down (direction +1)
    opp_direction = -1 if opponent == "WHITE" else 1

    # Our home row is the back row we started on
    home_row = 7 if player == "WHITE" else 0

    # Running totals for each feature we care about
    own_pieces = 0        # how many of our pieces are alive
    opp_advanced = 0      # how far enemy pieces have marched into our territory
    own_under_attack = 0  # how many of our pieces an enemy can capture next turn
    own_connected_h = 0   # how many pairs of our pieces are touching side by side
    own_home_row = 0      # how many of our pieces are still on our starting row

    for r in range(8):
        for c in range(8):
            cell = board[r][c]

            if cell == player:
                own_pieces += 1

                # Check if this piece is on our home row
                if r == home_row:
                    own_home_row += 1

                # Check if the piece directly to our right is also ours (horizontal connection)
                if c + 1 < 8 and board[r][c + 1] == player:
                    own_connected_h += 1

                # Check if an enemy piece is sitting diagonally behind us (ready to capture)
                # The enemy attacks from the row they just moved from, which is one step
                # opposite to their forward direction
                attack_row = r - opp_direction
                if 0 <= attack_row < 8:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and board[attack_row][nc] == opponent:
                            own_under_attack += 1
                            break  # No need to check the other diagonal once we know we're threatened

            elif cell == opponent:
                # Measure how many rows the enemy piece has traveled from its starting rows.
                # WHITE starts near row 7, BLACK starts near row 0.
                if opponent == "WHITE":
                    advancement = 7 - r   # WHITE starts at rows 6-7; row 0 = fully advanced
                else:
                    advancement = r       # BLACK starts at rows 0-1; row 7 = fully advanced
                opp_advanced += advancement

    # Add everything up using weights that reflect how important each factor is
    score = (
        3.0 * own_pieces          # staying alive matters most
        - 2.5 * opp_advanced      # bad if enemy is deep in our side
        - 1.5 * own_under_attack  # bad if our pieces are about to be taken
        + 1.0 * own_connected_h   # good to have pieces protecting each other
        + 2.0 * own_home_row      # good to keep our back row defended
        + random.random()         # tiny random value to break ties
    )
    return score


def offensive_eval_2(state, player):
    """
    Offensive Evaluation 2: A smarter offensive score designed to beat Defensive Eval 1.

    Instead of just counting enemy losses, we look at:
    - How far our pieces have moved toward the enemy home row (more = better)
    - Whether any of our pieces are one step away from winning AND safe from capture (huge bonus)
    - How many enemy pieces are still alive (fewer = better)
    - How many of our pieces are not currently threatened (more = better)

    We multiply each factor by a weight and add them all up.
    """
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # The direction the opponent moves (so we can check if they threaten our pieces)
    opp_direction = -1 if opponent == "WHITE" else 1

    # The row that is ONE step away from the enemy's home row (almost a win!)
    # WHITE wins by reaching row 0, so row 1 is almost there.
    # BLACK wins by reaching row 7, so row 6 is almost there.
    almost_win_row = 1 if player == "WHITE" else 6

    # Running totals
    own_advancement = 0  # total distance all our pieces have traveled forward
    almost_win = 0       # pieces that are one step from winning and are safe
    opp_pieces = 0       # how many enemy pieces are still alive
    own_pieces_safe = 0  # how many of our pieces are NOT about to be captured

    for r in range(8):
        for c in range(8):
            cell = board[r][c]

            if cell == player:
                # How many rows has this piece traveled from its starting position?
                # WHITE starts near row 7, so being on row 0 means it traveled 7 rows.
                # BLACK starts near row 0, so being on row 7 means it traveled 7 rows.
                if player == "WHITE":
                    advancement = 7 - r
                else:
                    advancement = r
                own_advancement += advancement

                # Check if this piece is on the "almost win" row AND safe from capture
                if r == almost_win_row:
                    attack_row = r - opp_direction
                    under_attack = False
                    if 0 <= attack_row < 8:
                        for dc in [-1, 1]:
                            nc = c + dc
                            if 0 <= nc < 8 and board[attack_row][nc] == opponent:
                                under_attack = True
                                break
                    if not under_attack:
                        almost_win += 1  # This piece could win on the very next move!

                # Check if this piece is safe right now (no enemy can capture it next turn)
                attack_row = r - opp_direction
                under_attack = False
                if 0 <= attack_row < 8:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and board[attack_row][nc] == opponent:
                            under_attack = True
                            break
                if not under_attack:
                    own_pieces_safe += 1

            elif cell == opponent:
                opp_pieces += 1

    # Add everything up using weights
    score = (
        2.0 * own_advancement        # reward pushing pieces forward
        + 6.0 * almost_win           # huge reward for pieces one step from winning
        + 2.0 * (32 - opp_pieces)    # reward having fewer enemies left
        + 0.5 * own_pieces_safe      # small reward for pieces that are safe to keep moving
        + random.random()            # tiny random value to break ties
    )
    return score


ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for competition.

##########################################################################


def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False):  # ⚠️ DO NOT CHANGE
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
        # Ask the correct agent to pick a move depending on whose turn it is
        move = (
            white_agent.select_move(game, state)
            if state["to_move"] == "WHITE"
            else black_agent.select_move(game, state)
        )
        state = game.result(state, move)  # Apply the move and get the new board state
        if display:
            game.display(state)           # Print the board after every move if display is on
        move_count += 1
        if progress:
            pbar.update()
        # Stop the loop if someone won or we hit the move limit
        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                # The player who just moved is the winner (the other player is now "to_move")
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None  # No winner — the game went on too long
            break
    if progress:
        pbar.close()

    # Calculate summary statistics from the move logs each agent kept
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = sum(white_agent.time_per_move) / len(white_agent.time_per_move)
    black_time_per_move = sum(black_agent.time_per_move) / len(black_agent.time_per_move)
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state["captures"]["WHITE"]
    black_captures = state["captures"]["BLACK"]
    if display:
        game.display(state)
    return {
        "winner": "white" if winner == "WHITE" else "black" if winner == "BLACK" else None,
        "white_name": white_agent.name,
        "black_name": black_agent.name,
        "total_moves": move_count,
        "white_nodes": white_nodes,
        "black_nodes": black_nodes,
        "white_nodes_per_move": white_nodes_per_move,
        "black_nodes_per_move": black_nodes_per_move,
        "white_time_per_move": white_time_per_move,
        "black_time_per_move": black_time_per_move,
        "white_captures": white_captures,
        "black_captures": black_captures,
    }


if __name__ == "__main__":
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)