import random
from copy import deepcopy, copy

from tqdm import tqdm

from games import Game


# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self):  # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",  # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0},  # Initially, white and black have captured 0 pieces.
            'board': grid,  # 8x8 grid representing the board.
        }  # ⚠️ You must use this structure for the state representation.

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
        current_player = state['to_move']
        board = state['board']
        move_list = []
        # print("Doing search")
        if current_player == 'WHITE':
            # Scan the grid 2d array to find the white pieces.
            for r in range(0, 8):
                for c in range(0, 8):
                    if board[r][c] == "WHITE":
                        # We check the possible move of this White piece.
                        # First, suppose it is not going out of the board. We take care of the diagonal traveling first.
                        # White pieces need to go up
                        newy = r - 1
                        left = c - 1
                        right = c + 1
                        if r - 1 >= 0:
                            if c - 1 >= 0:
                                target = board[newy][left]
                                if target == "EMPTY" or target == "BLACK":
                                    move_list.append({'from': (r, c), 'to': (newy, left)})

                            if c + 1 < 8:
                                target = board[newy][right]
                                if target == "EMPTY" or target == "BLACK":
                                    move_list.append({'from': (r, c), 'to': (newy, right)})

                            if board[newy][c] == "EMPTY":
                                move_list.append({'from': (r, c), 'to': (newy, c)})
            return move_list
        elif current_player == 'BLACK':
            # find the Black pieces.
            for r in range(0, 8):
                for c in range(0, 8):
                    if board[r][c] == "BLACK":
                        newy = r + 1
                        left = c - 1
                        right = c + 1
                        if r + 1 <= 7:
                            if c - 1 >= 0:
                                target = board[newy][left]
                                if target == "EMPTY" or target == "WHITE":
                                    move_list.append({'from': (r, c), 'to': (newy, left)})

                            if c + 1 < 8:
                                target = board[newy][right]
                                if target == "EMPTY" or target == "WHITE":
                                    move_list.append({'from': (r, c), 'to': (newy, right)})

                            if board[newy][c] == "EMPTY":
                                move_list.append({'from': (r, c), 'to': (newy, c)})
            return move_list

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
        new_state = deepcopy(state)
        current_player = new_state['to_move']
        start_piece = action['from']
        end_piece = action['to']
        cap = new_state['captures']
        my_game = new_state['board']

        if current_player == 'WHITE':
            current_player = 'BLACK'
            my_game[start_piece[0]][start_piece[1]] = 'EMPTY'
            # Read the (from, to) pair of action
            if my_game[end_piece[0]][end_piece[1]] == 'BLACK':
                cap['WHITE'] += 1
                my_game[end_piece[0]][end_piece[1]] = 'WHITE'
            else:
                my_game[end_piece[0]][end_piece[1]] = 'WHITE'
        elif current_player == 'BLACK':
            current_player = 'WHITE'
            my_game[start_piece[0]][start_piece[1]] = 'EMPTY'
            if my_game[end_piece[0]][end_piece[1]] == 'WHITE':
                cap['BLACK'] += 1
                my_game[end_piece[0]][end_piece[1]] = 'BLACK'
            else:
                my_game[end_piece[0]][end_piece[1]] = 'BLACK'

        else:
            print("Can't accept Pink doing RESULTS ya know?")
            return False
        return {
            'to_move': current_player,  # Player is also a string "WHITE" or "BLACK".
            'captures': cap,  # Initially, white and black have captured 0 pieces.
            'board': my_game,  # 8x8 grid representing the board.
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

        if self.to_move(state) == player:
            return -90
        else:
            return 90

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        my_game = state['board']
        white_count = 0
        black_count = 0
        for r in range(0, 8):
            for c in range(0, 8):
                if my_game[r][c] == 'WHITE':
                    white_count += 1
                elif my_game[r][c] == 'BLACK':
                    black_count += 1

        if white_count == 0 or black_count == 0:
            return True

        for c in range(0, 8):
            if my_game[0][c] == 'WHITE' or my_game[7][c] == 'BLACK':
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
        print(
            f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    friendly = 0
    for r in range(0, 8):
        for c in range(0, 8):
            if state['board'][r][c] == player:
                friendly += 1

    return 2 * friendly + random.random()


def offensive_eval_1(state, player):
    enemy = 0
    for r in range(0, 8):
        for c in range(0, 8):
            if state['board'][r][c] != player and state['board'][r][c] != 'EMPTY':
                enemy += 1

    return 2 * (32 - enemy) + random.random()


def defensive_eval_2(state, player):
    white_piece_coord = []
    black_piece_coord = []
    my_game = state['board']
    for r in range(0, 8):
        for c in range(0, 8):
            if my_game[r][c] == 'WHITE':
                white_piece_coord.append([r, c])

            elif my_game[r][c] == 'BLACK':
                black_piece_coord.append([r, c])
    r = 0
    c = 0

    def pieceAlmostWin(my_board, current):
        """Is there a friendly piece almost reaching the end?"""
        if current == 'WHITE':
            for c in range(0, 8):
                if my_board[1][c] == 'WHITE':
                    return 1
            return 0
        else:
            for c in range(0, 8):
                if my_board[7][c] == 'BLACK':
                    return 1
            return 0

    def almostLost(my_board, current):
        if current == 'WHITE':
            for c in range(0, 8):
                if my_board[6][c] == 'BLACK':
                    return 1
        else:
            for c in range(0, 8):
                if my_board[1][c] == 'WHITE':
                    return 1
        return 0

    def pieceHomeGround(my_board, current):
        """Ranges from 0 to 16"""
        guard_count = 0
        if current == 'WHITE':
            for r in range(6, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        guard_count += 1
        else:
            for r in range(0, 2):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        guard_count += 1
        return guard_count + random.random()

    def countEnemy(my_board, current):
        enemy = 0
        for r in range(0, 8):
            for c in range(0, 8):
                if my_board[r][c] != current and my_board[r][c] != 'EMPTY':
                    enemy += 1

        return 2 * (32 - enemy) + random.random()

    def pieceConnectHorizontal(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0], piece[1] + 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] + 1])
                    temp_white.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] - 1])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0], piece[1] + 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] + 1])
                    temp_black.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] - 1])
                    temp_black.remove(piece)

        return pairs + random.random()

    def pieceConnectVertical(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0] + 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] + 1, piece[1]])
                    temp_white.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] - 1, piece[1]])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0] + 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] + 1, piece[1]])
                    temp_black.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] - 1, piece[1]])
                    temp_black.remove(piece)

        return pairs + random.random()

    def pieceUnderAttack(white_piece, black_piece, current):
        """How many pieces are currently under attack"""
        # Should return a value from 0 to 12.

        danger = 0
        if current == 'WHITE':
            for piece in white_piece:
                # Search for an attacker
                if [piece[0] - 1, piece[1] + 1] in black_piece or [piece[0] - 1, piece[1] - 1] in black_piece:
                    danger += 1

        else:
            for piece in black_piece:
                if [piece[0] + 1, piece[1] + 1] in white_piece or [piece[0] + 1, piece[1] - 1] in white_piece:
                    danger += 1
        return danger + random.random()

    def inEnemy(my_board, current):
        """How many friendlies are in the my_game's other half of the board"""
        # Reasonably this value should be between 0 and 12 pieces
        count = 0
        if current == 'WHITE':
            for r in range(0, 4):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        count += 1
        else:
            for r in range(4, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        count += 1
        return count + random.random()

    def moveDistance(white_piece, black_piece, current):
        # Count the collective move distance of the four pioneering pieces.
        # This should return a value that is reasonably between 0 and 15
        distance = 0
        if current == 'WHITE':
            if len(white_piece) >= 4:
                for i in range(0, 4):
                    # Distance from row 2
                    distance += 6 - white_piece_coord[i][0]

            else:
                for i in range(len(white_piece)):
                    distance += 6 - white_piece_coord[i][0]
        else:
            if len(black_piece) >= 4:
                for i in range(len(black_piece) - 4, len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

            else:
                for i in range(len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

        return distance + random.random()

    aw_weight = 5
    al_weight = 20
    hg_weight = 2
    ch_weight = 1
    vt_weight = 1
    uaa_weight = 5
    ie_weight = 1
    md_weight = 0.5
    return aw_weight * pieceAlmostWin(my_game, player) + -1 * al_weight * almostLost(my_game,
                                                                                     player) + hg_weight * pieceHomeGround(
        my_game, player) + ch_weight * pieceConnectHorizontal(white_piece_coord, black_piece_coord,
                                                              player) + vt_weight * pieceConnectVertical(
        white_piece_coord, black_piece_coord, player) + -1 * uaa_weight * pieceUnderAttack(white_piece_coord,
                                                                                           black_piece_coord,
                                                                                           player) + ie_weight * inEnemy(
        my_game, player) + md_weight * moveDistance(white_piece_coord, black_piece_coord, player)


def offensive_eval_2(state, player):
    white_piece_coord = []
    black_piece_coord = []
    my_game = state['board']
    for r in range(0, 8):
        for c in range(0, 8):
            if my_game[r][c] == 'WHITE':
                white_piece_coord.append([r, c])

            elif my_game[r][c] == 'BLACK':
                black_piece_coord.append([r, c])
    r = 0
    c = 0

    def countEnemy(my_board, current):
        enemy = 0
        for r in range(0, 8):
            for c in range(0, 8):
                if my_board[r][c] != current and my_board[r][c] != 'EMPTY':
                    enemy += 1

        return 2 * (32 - enemy) + random.random()

    def pieceAlmostWin(my_board, current):
        """Is there a friendly piece almost reaching the end?"""
        if current == 'WHITE':
            for c in range(0, 8):
                if my_board[1][c] == 'WHITE':
                    return 1
            return 0
        else:
            for c in range(0, 8):
                if my_board[7][c] == 'BLACK':
                    return 1
            return 0

    def pieceHomeGround(my_board, current):
        """Ranges from 0 to 16"""
        guard_count = 0
        if current == 'WHITE':
            for r in range(6, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        guard_count += 1
        else:
            for r in range(0, 2):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        guard_count += 1
        return guard_count + random.random()

    def pieceConnectHorizontal(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0], piece[1] + 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] + 1])
                    temp_white.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] - 1])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0], piece[1] + 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] + 1])
                    temp_black.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] - 1])
                    temp_black.remove(piece)

        return pairs + random.random()

    def pieceConnectVertical(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0] + 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] + 1, piece[1]])
                    temp_white.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] - 1, piece[1]])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0] + 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] + 1, piece[1]])
                    temp_black.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] - 1, piece[1]])
                    temp_black.remove(piece)

        return pairs + random.random()

    def underAttackAggressive(white_piece, black_piece, current):
        """How many pieces are currently under attack, with weights on the pioneers"""
        # This function should return a value between 0 and 14.
        danger = 0
        if current == 'WHITE':
            if len(white_piece) < 3:
                for piece in white_piece:
                    if [piece[0] - 1, piece[1] + 1] in black_piece or [piece[0] - 1, piece[1] - 1] in black_piece:
                        danger += 3
                return danger
            else:
                for i in range(len(white_piece)):
                    if i < 2:
                        if [white_piece[i][0] - 1, white_piece[i][1] + 1] in black_piece or [white_piece[i][0] - 1,
                                                                                             white_piece[i][
                                                                                                 1] - 1] in black_piece:
                            danger += 3
                    else:
                        if [white_piece[i][0] - 1, white_piece[i][1] + 1] in black_piece or [white_piece[i][0] - 1,
                                                                                             white_piece[i][
                                                                                                 1] - 1] in black_piece:
                            danger += 1
        else:
            if len(black_piece) < 3:
                for piece in black_piece:
                    if [piece[0] + 1, piece[1] + 1] in white_piece or [piece[0] + 1, piece[1] - 1] in white_piece:
                        danger += 3
                return danger
            else:
                for i in range(len(black_piece)):
                    if i < len(black_piece) - 2:
                        if [black_piece[i][0] + 1, black_piece[i][1] + 1] in white_piece or [black_piece[i][0] + 1,
                                                                                             black_piece[i][
                                                                                                 1] - 1] in white_piece:
                            danger += 3
                    else:
                        if [black_piece[i][0] + 1, black_piece[i][1] + 1] in white_piece or [black_piece[i][0] + 1,
                                                                                             black_piece[i][
                                                                                                 1] - 1] in white_piece:
                            danger += 1
        return danger + random.random()

    def inEnemy(my_board, current):
        """How many friendlies are in the my_game's other half of the board"""
        # Reasonably this value should be between 0 and 12 pieces
        count = 0
        if current == 'WHITE':
            for r in range(0, 4):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        count += 1
        else:
            for r in range(4, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        count += 1
        return count + random.random()

    def moveDistance(white_piece, black_piece, current):
        # Count the collective move distance of the four pioneering pieces.
        # This should return a value that is reasonably between 0 and 15
        distance = 0
        if current == 'WHITE':
            if len(white_piece) >= 4:
                for i in range(0, 4):
                    # Distance from row 2
                    distance += 6 - white_piece_coord[i][0]

            else:
                for i in range(len(white_piece)):
                    distance += 6 - white_piece_coord[i][0]
        else:
            if len(black_piece) >= 4:
                for i in range(len(black_piece) - 4, len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

            else:
                for i in range(len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

        return distance + random.random()

    aw_weight = 10
    hg_weight = 0.5
    ch_weight = 2
    vt_weight = 0.5
    uaa_weight = 2
    ie_weight = 1
    md_weight = 2
    ct_enemy = 0.25
    return aw_weight * pieceAlmostWin(my_game, player) + hg_weight * pieceHomeGround(
        my_game, player) + ch_weight * pieceConnectHorizontal(white_piece_coord, black_piece_coord,
                                                              player) + vt_weight * pieceConnectVertical(
        white_piece_coord, black_piece_coord, player) + -1 * uaa_weight * underAttackAggressive(white_piece_coord,
                                                                                                black_piece_coord,
                                                                                                player) + ie_weight * inEnemy(
        my_game, player) + md_weight * moveDistance(white_piece_coord, black_piece_coord,
                                                    player) + ct_enemy * countEnemy(my_game, player)


def defensive_eval_test(state, player):
    white_piece_coord = []
    black_piece_coord = []
    my_game = state['board']
    for r in range(0, 8):
        for c in range(0, 8):
            if my_game[r][c] == 'WHITE':
                white_piece_coord.append([r, c])

            elif my_game[r][c] == 'BLACK':
                black_piece_coord.append([r, c])
    r = 0
    c = 0

    def pieceAlmostWin(my_board, current):
        """Is there a friendly piece almost reaching the end?"""
        if current == 'WHITE':
            for c in range(0, 8):
                if my_board[1][c] == 'WHITE':
                    return 1
            return 0
        else:
            for c in range(0, 8):
                if my_board[7][c] == 'BLACK':
                    return 1
            return 0

    def almostLost(my_board, current):
        if current == 'WHITE':
            for c in range(0, 8):
                if my_board[6][c] == 'BLACK':
                    return 1
        else:
            for c in range(0, 8):
                if my_board[1][c] == 'WHITE':
                    return 1
        return 0

    def pieceHomeGround(my_board, current):
        """Ranges from 0 to 16"""
        guard_count = 0
        if current == 'WHITE':
            for r in range(6, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        guard_count += 1
        else:
            for r in range(0, 2):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        guard_count += 1
        return guard_count

    def countEnemy(my_board, current):
        enemy = 0
        for r in range(0, 8):
            for c in range(0, 8):
                if my_board[r][c] != current and my_board[r][c] != 'EMPTY':
                    enemy += 1

        return 2 * (32 - enemy)

    def pieceConnectHorizontal(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0], piece[1] + 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] + 1])
                    temp_white.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0], piece[1] - 1])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0], piece[1] + 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] + 1])
                    temp_black.remove(piece)
                elif [piece[0], piece[1] - 1] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0], piece[1] - 1])
                    temp_black.remove(piece)

        return pairs

    def pieceConnectVertical(white_piece, black_piece, current):
        """Ranges from 0 to 8"""
        pairs = 0
        if current == 'WHITE':
            temp_white = deepcopy(white_piece)
            for piece in temp_white:
                if [piece[0] + 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] + 1, piece[1]])
                    temp_white.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_white:
                    pairs += 1
                    temp_white.remove([piece[0] - 1, piece[1]])
                    temp_white.remove(piece)
        else:
            temp_black = deepcopy(black_piece)
            for piece in temp_black:
                if [piece[0] + 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] + 1, piece[1]])
                    temp_black.remove(piece)
                elif [piece[0] - 1, piece[1]] in temp_black:
                    pairs += 1
                    temp_black.remove([piece[0] - 1, piece[1]])
                    temp_black.remove(piece)

        return pairs

    def pieceUnderAttack(white_piece, black_piece, current):
        """How many pieces are currently under attack"""
        # Should return a value from 0 to 12.

        danger = 0
        if current == 'WHITE':
            for piece in white_piece:
                # Search for an attacker
                if [piece[0] - 1, piece[1] + 1] in black_piece or [piece[0] - 1, piece[1] - 1] in black_piece:
                    danger += 1

        else:
            for piece in black_piece:
                if [piece[0] + 1, piece[1] + 1] in white_piece or [piece[0] + 1, piece[1] - 1] in white_piece:
                    danger += 1
        return danger

    def inEnemy(my_board, current):
        """How many friendlies are in the my_game's other half of the board"""
        # Reasonably this value should be between 0 and 12 pieces
        count = 0
        if current == 'WHITE':
            for r in range(0, 4):
                for c in range(0, 8):
                    if my_board[r][c] == 'WHITE':
                        count += 1
        else:
            for r in range(4, 8):
                for c in range(0, 8):
                    if my_board[r][c] == 'BLACK':
                        count += 1
        return count

    def moveDistance(white_piece, black_piece, current):
        # Count the collective move distance of the four pioneering pieces.
        # This should return a value that is reasonably between 0 and 15
        distance = 0
        if current == 'WHITE':
            if len(white_piece) >= 4:
                for i in range(0, 4):
                    # Distance from row 2
                    distance += 6 - white_piece_coord[i][0]

            else:
                for i in range(len(white_piece)):
                    distance += 6 - white_piece_coord[i][0]
        else:
            if len(black_piece) >= 4:
                for i in range(len(black_piece) - 4, len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

            else:
                for i in range(len(black_piece)):
                    distance += black_piece_coord[i][0] - 1

        return distance

    aw_weight = 5
    al_weight = 15
    hg_weight = 2
    ch_weight = 1
    vt_weight = 1
    uaa_weight = 5
    ie_weight = 1
    md_weight = 0.5
    return aw_weight * pieceAlmostWin(my_game, player) + -1 * al_weight * almostLost(my_game,
                                                                                     player) + hg_weight * pieceHomeGround(
        my_game, player) + ch_weight * pieceConnectHorizontal(white_piece_coord, black_piece_coord,
                                                              player) + vt_weight * pieceConnectVertical(
        white_piece_coord, black_piece_coord, player) + -1 * uaa_weight * pieceUnderAttack(white_piece_coord,
                                                                                           black_piece_coord,
                                                                                           player) + ie_weight * inEnemy(
        my_game, player) + md_weight * moveDistance(white_piece_coord, black_piece_coord, player)


ag_eval_fn = offensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.


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
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game,
                                                                                                                state)
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
    # white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    # black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_2)
    white_agent = MinimaxAgent("Minimax Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = MinimaxAgent("Minimax Def1", depth=3, eval_fn=offensive_eval_2)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
