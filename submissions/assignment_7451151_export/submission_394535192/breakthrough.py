import math
import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

from copy import deepcopy

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
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]

        # Extract White or Black
        player_to_move = state["to_move"]
        # Know our opponent
        opponent = "WHITE" if player_to_move == "BLACK" else "BLACK"
        # Get our board
        board = state["board"]
        # How many White (or) Black players are left
        players_left = 16 - state["captures"][opponent]
        # List of possible actions
        possible_actions = []

        # Counter to decide if we need to add more players
        player_count = 0
        # Calibrate our board (Optimized for beginning of game though)
        if player_to_move == "WHITE":  # Upper numbers first
            start_row = 7
            acc = -1
        elif player_to_move == "BLACK":  # Lower numbers first
            start_row = 0
            acc = 1
        # Scanner accumulator; goes through entire board to look for needed pieces
        scan_state = [start_row, 0]
        # For each player:
        while player_count < players_left:
            # Find players and select their legal moves
            # Get current item
            curr_item = board[scan_state[0]][scan_state[1]]

            # If item is the moving player
            if curr_item == player_to_move:
                # Get the leftmost forward locations(put one back, increment at beginning of array)
                curr_location = [scan_state[0] + acc, scan_state[1] - 2]
                # curr_location = first_location

                # Count how many locations we have traveled(put one back, increment at beginning of array)
                loc_count = -1

                # Loop through the three forward locations going right(put one back, increment at beginning of array)
                while loc_count < 2:
                    # Increase location count(put at front because of continue
                    loc_count += 1
                    curr_location[1] += 1

                    # Check valid location
                    # Criterion is: Bounds, Friendly Player, Opponent In Front
                    out_of_bounds = 0 > curr_location[1] or curr_location[1] >= 8
                    # friendly_player = False # Declare first(in out-of-bounds squares)
                    if not out_of_bounds:
                        # Check only if not out of bounds(prevent crashing error)
                        friendly_player = board[curr_location[0]][curr_location[1]] == player_to_move

                    # Check criterion
                    if out_of_bounds or friendly_player:
                        # break out if true
                        continue

                    # Opponent in front only matters for the 2nd location
                    if loc_count == 1:
                        # Find the element in front of the piece
                        opponent_in_front = board[curr_location[0]][curr_location[1]] == opponent
                        # If opponent is in front of current player
                        if opponent_in_front:
                            # Break out of loop
                            continue

                    # If all tests passed, move is valid
                    possible_actions.append({"from": tuple(scan_state), "to": tuple(curr_location)})

                player_count += 1

            # Update our scan state
            scan_state[1] = (scan_state[1] + 1) % 8
            # If we are resetting board
            if scan_state[1] == 0:
                scan_state[0] = scan_state[0] + acc

            # Guard for if scan_state[0] is out of bounds(-1 or 8)
            if scan_state[0] < 0 or scan_state[0] >= 8:
                break

        # if len(possible_actions) == 0:
        #     print()

        # Return all our possible actions
        return possible_actions

    def result(self, state, action):
        ##########################################################################
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).

        # Extract variables from state
        to_move = state["to_move"]
        captures = deepcopy(state["captures"])
        board =  deepcopy(state["board"])

        # Extract variables from action
        start = action["from"]
        dest = action["to"]

        # Get start/end items
        dest_item = board[dest[0]][dest[1]]

        # Given: Update old to blank, and new to player square
        board[start[0]][start[1]] = "EMPTY"
        board[dest[0]][dest[1]] = to_move

        # If resulting action square is blank, don't do anything extra
        # If resulting square was opponent, then add to our captured pieces
        opponent = "WHITE" if to_move == "BLACK" else "BLACK"
        if dest_item == opponent:
            captures[to_move] += 1

        return {"to_move": opponent, "captures": captures, "board": board}


    def utility(self, state, player):
        ##########################################################################
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        board = state["board"]
        captures = state["captures"]

        winner = "EMPTY"

        # Check if all pieces are captured for one or other
        if captures["WHITE"] ==  16:
            return 1 if player == "WHITE" else -1
        elif captures["BLACK"] == 16:
            return 1 if player == "BLACK" else -1

        # Check top/bottom row
        # Top(lower numbers) for white, bottom(higher numbers) for black
        for i in range(8):
            if board[7][i] == "BLACK":
                winner = "BLACK"
            if board[0][i] == "WHITE":
                winner = "WHITE"

        # Check who winner is
        if winner == "EMPTY":
            return 0
        else:
            if winner == player:
                return 1
            else:
                return -1

    def terminal_test(self, state):
        ##########################################################################
        # Return True if this is a terminal state, False otherwise.
        if self.utility(state, "WHITE") == 0:
            return False
        else:
            return True


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
# Evaluation functions

def defensive_eval_1(state, player):
    players_captured = state["captures"]
    opposing_player = "WHITE" if player == "BLACK" else "BLACK"

    num_pieces_remaining = 16 - players_captured[opposing_player]

    # if (num_pieces_remaining == 11):
    #     print()
    
    return 2 * num_pieces_remaining + random.random()


def offensive_eval_1(state, player):
    players_captured = state["captures"]

    opp_pieces_remaining = 16 - players_captured[player]
    
    return 2 * (32 - opp_pieces_remaining) + random.random()


def defensive_eval_2(state, player):
    players_captured = state["captures"]
    opposing_player = "WHITE" if player == "BLACK" else "BLACK"

    num_pieces_remaining = 16 - players_captured[opposing_player]

    piece_remain_count = 2 * num_pieces_remaining

    offensive_danger_value = player_danger_value(state, opposing_player, True)

    security_value = home_row_security(state, player)
    
    return piece_remain_count + offensive_danger_value + security_value


def offensive_eval_2(state, player):
    players_captured = state["captures"]

    opp_pieces_remaining = 16 - players_captured[player]

    piece_capture_count =  2 * (32 - opp_pieces_remaining)

    almost_win = 1000 * piece_almost_win(state, player)

    offensive_danger_value = player_danger_value(state, player, True)
    
    return piece_capture_count + almost_win + offensive_danger_value

def piece_almost_win(state, player):
    # Get our board
    board = state["board"]

    # Decide our row to scan
    if player == "WHITE":
        almostRow = 1
        forward = -1
    elif player == "BLACK":
        almostRow = 6
        forward = 1

    # Decide our opponent
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # Loop through the almost row
    for i in range(8):
        # If the current player is almost winning
        if board[almostRow][i] == player:
            return 0 if piece_under_attack(state, (almostRow, i)) else 1

    # If we don't have a player
    return 0

def player_danger_value(state, player, op):
    board = state["board"]

    if player == "WHITE":
        row = 5
        forward = -1
    elif player == "BLACK":
        row = 2
        forward = 1

    opponent = "BLACK" if player == "WHITE" else "WHITE"

    total_danger = 0

    # For all rows after the first two
    for _ in range(6):
        # For each row location
        for j in range(8):
            # If we find a piece
            if board[row][j] == player:
                # Farther the piece is, it has a greater danger value

                # If we are calculating offensive player danger, piece under attack matters
                if op:
                    if piece_under_attack(state, (row, j)):
                        continue

                # Irrespective of color
                progress = row if player == "BLACK" else 7 - row

                total_danger += 10 * math.exp(0.77 * (progress - 3)) + 7.4

        # Update our row value
        row += forward

    return total_danger

def home_row_security(state, player):
    board = state["board"]

    if player == "WHITE":
        row = 7
        forward = -1
    elif player == "BLACK":
        row = 0
        forward = 1

    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # Keep track of our empty streaks
    empty_streak_1 = 0
    empty_streak_2 = 0

    # Get our scorers
    security_score = 0
    never_one = True
    never_two = True

    # For the first two rows
    for i in range(8):
        # See if the item is our player or an empty space
        # If we have 3 or more empty spaces that is not good but doable
        # If we have 3 or more empty spaces for both rows at the same time that is not good

        # Check our items
        if board[row][i] == player:
            empty_streak_1 = 0
        elif board[row][i] == "EMPTY":
            empty_streak_1 += 1

        if board[row + forward][i] == player:
            empty_streak_2 = 0
        elif board[row + forward][i] == "EMPTY":
            empty_streak_2 += 1
        elif board[row + forward][i] == opponent:
            ...

        # Assign security scores for holes
        if empty_streak_1 >= 3:
            never_one = False
            security_score -= 15
        if empty_streak_2 >= 3:
            never_one = False
            security_score -= 15
        if empty_streak_1 >= 3 and empty_streak_2 >= 3:
            never_two = False
            security_score -= 30

    if never_two:
        security_score += 30
    elif never_one:
        security_score += 15 # Effectively 0 because we lost for the other one(yes it is redundant)

    return security_score

def piece_under_attack(state, location):
    # Get our board
    board = state["board"]
    # Get our piece
    piece = board[location[0]][location[1]]
    # Get our opponent
    opponent = "BLACK" if piece == "WHITE" else "WHITE"

    # Guard for empty piece
    if piece == "EMPTY":
        return False

    # See where forward is
    if piece == "WHITE":
        forward = -1
    elif piece == "BLACK":
        forward = 1

    # If enemy pieces are diagonal to it
    diagonalSpots = []
    if location[1] > 0:
        diagonalSpots.append(board[location[0] + forward][location[1] - 1])
    if location[1] < 7:
        diagonalSpots.append(board[location[0] + forward][location[1] + 1])

    # Loop through our diagonal spots
    for spot in diagonalSpots:
        if spot == opponent:
            # True if piece under attack
            return True

    # If our piece wasn't under attack
    return False

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
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
