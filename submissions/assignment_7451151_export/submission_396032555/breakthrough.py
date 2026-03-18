# Rohan Gladson
# IP 2: Playing Breakthrough
# CS 4341: Introduction to Artificial Intelligence

import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to tic-tac-toe example for Breakthrough implementation.

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
        # With the "to_move function" we are having it where
        # the state dictionary stores whose turn it currently is
        # under the key "to_move".
        #
        # Possible values are:
        #   "WHITE": white player should move
        #   "BLACK": black player should move
        #
        # Here what we are doing is simply returning this value so
        # the game framework knows which player's agent should act next.

        return state["to_move"]

    def actions(self, state):
        # What we are doing here in the "actions" function is generating
        # all legal moves for the player whose turn it is.

        board = state["board"]
        player = state["to_move"]

        # First, what we do is determine the opponent player
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        # Rule: Direction of movement depends on the player
        # WHITE: moves "up" the board (row decreases)
        # BLACK: moves "down" the board (row increases)
        direction = -1 if player == "WHITE" else 1

        moves = []

        # Scan every square on the board
        for r in range(8):
            for c in range(8):

                # Conditional, only consider pieces belonging to the current player
                if board[r][c] != player:
                    continue

                # Forward Move: Attempt to move forward by one square
                new_r = r + direction
                new_c = c

                # Check board boundary
                if 0 <= new_r < 8:
                    # Forward move is allowed only if the square is empty
                    if board[new_r][new_c] == "EMPTY":
                        moves.append({
                            "from": (r, c),
                            "to": (new_r, new_c)
                        })

                # Diagonal Moves: Diagonally move left and right
                for dc in [-1, 1]:

                    new_r = r + direction
                    new_c = c + dc

                    # Ensure the move stays inside board boundaries
                    if not (0 <= new_r < 8 and 0 <= new_c < 8):
                        continue

                    destination = board[new_r][new_c]

                    # Conditional for diagonal based move,
                    # it is legal if:
                    # - square is empty (normal move)
                    # - square contains an enemy piece (capture)
                    if destination == "EMPTY" or destination == enemy:
                        moves.append({
                            "from": (r, c),
                            "to": (new_r, new_c)
                        })
        return moves

    def result(self, state, action):
        # With the "results" function, we have it set up to where
        # the search algorithms will reuse the same states on more
        # than one occasion, so instead, we create a brand-new state object.

        # First what we do is copy the board deeply, give that
        # it is a nested list (8 lists of 8 strings).
        new_board = deepcopy(state["board"])

        # Afterward, we would then copy the captures dict so we can safely modify it.
        new_captures = dict(state["captures"])

        # Current player and opponent
        player = state["to_move"]
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        # Extract coordinates from the action dict
        (r1, c1) = action["from"]
        (r2, c2) = action["to"]

        # Sanity assumption: actions() only returns legal moves, so:
        # - (r1, c1) contains the player's piece
        # - (r2, c2) is either EMPTY or contains an enemy piece
        destination = new_board[r2][c2]

        # If we move onto an enemy piece, that is a capture.
        if destination == enemy:
            new_captures[player] += 1

        # Move the piece:
        # - Empty the origin square
        # - Place player's piece on the destination square (overwriting EMPTY or enemy)
        new_board[r1][c1] = "EMPTY"
        new_board[r2][c2] = player

        # Alternate turn to the other player
        next_player = enemy

        # Lastly, we would then return the new state in the exact
        # structure required by the template.
        return {
            "to_move": next_player,
            "captures": new_captures,
            "board": new_board
        }

    def utility(self, state, player):
        # Here with the "utility" function, it's primary purpose comes
        # when the game is over. Now, if there comes the case where
        # game is not over, we would return 0 so minimax uses eval_fn at cutoffs.

        board = state["board"]

        # Count remaining pieces of each color
        white_left = 0
        black_left = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_left += 1
                elif board[r][c] == "BLACK":
                    black_left += 1

        # Breakthrough conditions:
        # - WHITE wins if any WHITE piece reaches row 0 (top row)
        # - BLACK wins if any BLACK piece reaches row 7 (bottom row)
        white_breakthrough = any(board[0][c] == "WHITE" for c in range(8))
        black_breakthrough = any(board[7][c] == "BLACK" for c in range(8))

        # Elimination conditions:
        # - WHITE wins if BLACK has 0 pieces remaining
        # - BLACK wins if WHITE has 0 pieces remaining
        white_elimination_win = (black_left == 0)
        black_elimination_win = (white_left == 0)

        # Determine winner (if any)
        white_wins = white_breakthrough or white_elimination_win
        black_wins = black_breakthrough or black_elimination_win

        # Now, if neither side has won yet, this is a non-terminal state.
        if not white_wins and not black_wins:
            return 0

        # If both are true somehow, we will simply treat it as neutral.
        if white_wins and black_wins:
            return 0

        winner = "WHITE" if white_wins else "BLACK"

        # Return utility from the perspective of `player`
        return 1 if player == winner else -1

    def terminal_test(self, state):
        # Here with the "terminal_test" function, we have to where a state
        # is terminal if the game is finished.
        # The game ends when either of the following conditions are met:
        # - A piece reaches the opponent's home row ("breakthrough")
        # - All pieces of one player are captured (0 remaining).

        board = state["board"]

        # Breakthrough condition:
        # WHITE wins immediately, if any WHITE piece reaches the top row (row 0).
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True

        # BLACK wins immediately, if any BLACK piece reaches the bottom row (row 7).
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True

        # Elimination condition:
        # Count remaining pieces for both players.
        white_left = 0
        black_left = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_left += 1
                elif board[r][c] == "BLACK":
                    black_left += 1

        # If either player has no pieces left, the game is over.
        return white_left == 0 or black_left == 0

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
    # Defensive Eval 1: "The more pieces you have remaining, the higher your value is."

    # Formula:
    #   2 * (number_of_own_pieces_remaining) + random()

    board = state["board"]

    # Count how many pieces the current player still has on the board
    own_pieces = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1

    # Return the evaluation score with a small random tie-breaker
    return 2 * own_pieces + random.random()

def offensive_eval_1(state, player):
    # Offensive Eval 1: "The fewer pieces the opponent has remaining, the higher the value."
    #
    # Formula given in the assignment:
    #   2 * (32 - number_of_opponent_pieces_remaining) + random()

    board = state["board"]

    # Determine the opponent player
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # Count how many opponent pieces remain on the board
    opponent_pieces = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                opponent_pieces += 1

    # Compute evaluation score using the formula from the assignment
    score = 2 * (32 - opponent_pieces) + random.random()

    return score

def defensive_eval_2(state, player):
    # Defensive Eval 2:
    # The general basis surrounding this heuristic is that it is meant
    # to be more defensive than what we created earlier than Eval 1. So
    # here what I plan on having is instead of only rewarding "having
    # many of our own pieces left", it also tries to slow down the
    # opponent's progress toward our home row.

    # Essentially the main components of with this heuristic goes as follows:
    # - Reward keeping our own pieces alive.
    # - Reward captures we have already made.
    # - Penalize the opponent if they have advanced deeply into our territory.
    # - Add a small random value to break ties between equal-scoring positions.

    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    own_pieces = 0
    opponent_pieces = 0
    opponent_max_advance = 0

    # Count remaining pieces and measure the opponent's deepest advance.
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1
            elif board[r][c] == opponent:
                opponent_pieces += 1

                # For WHITE, the danger is BLACK moving downward toward row 7.
                # This would essentially mean that larger row index identifies
                # that BLACK is closer to WHITE's home row.
                if opponent == "BLACK":
                    advance = r

                # For BLACK, the danger is WHITE moving upward toward row 0.
                # This would essentially mean that smaller row index identifies
                # that WHITE is closer to BLACK's home row.
                else:
                    advance = 7 - r

                opponent_max_advance = max(opponent_max_advance, advance)

    # Captures already recorded in the state
    own_captures = state["captures"][player]

    # Now, the way in which we would go about heuristic scoring, would
    # go as follows:
    # - Strong reward for keeping our own pieces
    # - Some reward for captures
    # - Strong penalty if the opponent has advanced far toward our side
    score = (
            3 * own_pieces
            + 2 * own_captures
            - 2 * opponent_max_advance
            + random.random()
    )

    return score

def offensive_eval_2(state, player):
    # Offensive Eval 2:
    # The idea behind this heuristic is for it more aggressive than what we
    # had created earlier with evaluation 1. Here, what we are instead doing is
    # only rewarding positions where the opponent has fewer pieces. In this case
    # it also rewards pushing our own pieces forward toward a breakthrough.

    # Essentially the main components of with this heuristic goes as follows:
    # - Reward captures we have already made.
    # - Reward the furthest advanced piece (Essentially the strongest breakthrough threat).
    # - Reward total forward progress of all our pieces.
    # - Give a small bonus for still having our own pieces alive.
    # - Additionally to also add random noise to break ties.

    board = state["board"]

    own_pieces = 0
    own_captures = state["captures"][player]
    total_forward_progress = 0
    max_forward_progress = 0

    # Scan the board and in turn measure how aggressively our pieces
    # have advanced toward the opponent's home row.
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1

                # WHITE starts at the bottom and moves upward,
                # which would mean that smaller row index would
                # be more forward progress.
                if player == "WHITE":
                    # WHITE starts at bottom (rows 6–7) and moves upward
                    progress = 7 - r

                # BLACK starts at the top and moves downward,
                # which would mean so larger row index would be
                # more forward progress.
                else:
                    # BLACK starts at top (rows 0–1) and moves downward
                    progress = r

                total_forward_progress += progress
                max_forward_progress = max(max_forward_progress, progress)

    # Now, the way in which we would go about heuristic scoring, would
    # go as follows:
    # - Strong reward for captures
    # - Strong reward for having at least one deeply advanced piece
    # - Additional reward for overall board-wide forward pressure
    # - Small reward for still having our own pieces
    score = (
            3 * own_captures
            + 4 * max_forward_progress
            + 1 * total_forward_progress
            + 1 * own_pieces
            + random.random()
    )

    return score

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for competition.

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

    # To fix the warning: "Local variable 'pbar' might be referenced before assignment (Line 439)"
    # I went about initializing pbar so it always exists,
    # even when progress=False.
    pbar = None

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
    from breakthrough_agent import AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
