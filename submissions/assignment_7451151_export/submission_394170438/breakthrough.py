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
        # print(state["board"][0][0])
        list_of_moves = []
        current_player = state["to_move"]
        if current_player == "WHITE":
            for row in range(8):
                for col in range(8):
                    if (state["board"][row][col] == "WHITE" and row == 0):
                        # white piece at row 0, they can't go forward, skip it
                        continue

                    if state["board"][row][col] == "WHITE" and col == 0:
                        # white piece at the left edge
                        if state["board"][row-1][col] != "BLACK" and state["board"][row-1][col] != "WHITE":
                            # check the row in front
                            list_of_moves.append({"from": (row,col), "to": (row-1,col)})
                        if state["board"][row-1][col+1] != "WHITE":
                            # check the right diagonal
                            list_of_moves.append({"from": (row,col), "to": (row-1,col+1)})
                        continue

                    if state["board"][row][col] == "WHITE" and col == 7:
                        # white piece at the right edge
                        if state["board"][row-1][col] != "WHITE" and state["board"][row-1][col] != "BLACK":
                            # check for open piece in front
                            list_of_moves.append({"from": (row,col), "to": (row-1,col)})
                        if state["board"][row-1][col-1] != "WHITE":
                            # check that the left diagonal piece is not white
                            list_of_moves.append({"from": (row,col), "to": (row-1,col-1)})
                        continue
                    else:
                        # after checking all edge cases, proceed as normal
                        if state["board"][row][col] == "WHITE":
                            # white piece in a normal spot
                            if state["board"][row-1][col-1] != "WHITE":
                                # check that left diagonal is not white
                                list_of_moves.append({"from": (row,col), "to": (row-1,col-1)})
                            if state["board"][row-1][col] != "WHITE" and state["board"][row-1][col] != "BLACK":
                                # check the piece directly in front
                                list_of_moves.append({"from": (row,col), "to": (row-1,col)})
                            if state["board"][row-1][col+1] != "WHITE":
                                # check that the right diagonal is not white
                                list_of_moves.append({"from": (row,col), "to": (row-1,col+1)})

        elif current_player == "BLACK":
            for row in range(8):
                for col in range(8):
                    if (state["board"][row][col] == "BLACK" and row == 7):
                        # black piece at row 7, they can't go forward, skip it
                        continue

                    if state["board"][row][col] == "BLACK" and col == 0:
                        # black piece at the left edge
                        if state["board"][row+1][col] != "BLACK" and state["board"][row+1][col] != "WHITE":
                            # check for open piece in front
                            list_of_moves.append({"from": (row, col), "to": (row+1, col)})
                        if state["board"][row+1][col+1] != "BLACK":
                            # check the right diagonal
                            list_of_moves.append({"from": (row, col), "to": (row+1, col+1)})
                        continue

                    if state["board"][row][col] == "BLACK" and col == 7:
                        # black piece at the right edge
                        if state["board"][row+1][col] != "WHITE" and state["board"][row+1][col] != "BLACK":
                            # check for open piece in front
                            list_of_moves.append({"from": (row,col), "to": (row+1,col)})
                        if state["board"][row+1][col-1] != "BLACK":
                            # check that the left diagonal piece is not black
                            list_of_moves.append({"from": (row,col), "to": (row+1,col-1)})
                        continue
                    else:
                        # after checking all edge cases, proceed as normal
                        if state["board"][row][col] == "BLACK":
                            # black piece in a normal spot
                            if state["board"][row+1][col-1] != "BLACK":
                                # check that left diagonal is not white
                                list_of_moves.append({"from": (row,col), "to": (row+1,col-1)})
                            if state["board"][row+1][col] != "WHITE" and state["board"][row+1][col] != "BLACK":
                                # check the piece directly in front
                                list_of_moves.append({"from": (row,col), "to": (row+1,col)})
                            if state["board"][row+1][col+1] != "BLACK":
                                # check that the right diagonal is not black
                                list_of_moves.append({"from": (row,col), "to": (row+1,col+1)})
        return list_of_moves

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

        current_player = state["to_move"]
        from_row, from_col = action["from"] # coordinates of where the current player came from
        to_row, to_col = action["to"] # coordinates of where the current player will move to

        new_state = deepcopy(state)
        if current_player == "WHITE" and new_state["board"][to_row][to_col] == "BLACK":
            # white is capturing a black piece, increment whites captures by 1
            new_state["captures"]["WHITE"] += 1
        elif current_player == "BLACK" and new_state["board"][to_row][to_col] == "WHITE":
            # black is capturing a white piece, increment blacks captures by 1
            new_state["captures"]["BLACK"] += 1

        # now update the board
        new_state["board"][from_row][from_col] = "EMPTY"
        new_state["board"][to_row][to_col] = current_player

        # alternate the player to move
        if current_player == "WHITE":
            new_state["to_move"] = "BLACK"
        else:
            new_state["to_move"] = "WHITE"

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
        if state["to_move"] == player:
            # The next player to move after the game is the current one, so they lost
            return -1
        else:
            # The next player to move after the game is over is not the current one, so they won
            return 1


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        num_in_win_spots = 0
        num_white = 0
        num_black = 0
        actions = self.actions(state)
        if actions is None:
            return True

        for _ in state["board"][0]:
            # loop through the first row of the board
            if _ == "WHITE":
                num_in_win_spots += 1
        if num_in_win_spots == 8 or num_in_win_spots == 16 - state["captures"]["BLACK"]:
            # all white pieces in the first row, game over
            return True

        num_in_win_spots = 0
        for _ in state["board"][7]:
            # loop through the last row of the board
            if _ == "BLACK":
                num_in_win_spots += 1
        if num_in_win_spots == 8 or num_in_win_spots == 16 - state["captures"]["WHITE"]:
            # all black pieces in the back row, game over
            return True

        for row in range(8):
            for col in range(8):
                if state["board"][row][col] == "BLACK":
                    num_black += 1
                elif state["board"][row][col] == "WHITE":
                    num_white += 1

                if num_black >= 1 and num_white >= 1:
                    # Not all pieces captured, game not over
                    return False
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
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):

    if player == "WHITE":
        num_pieces_left = 16 - state["captures"]["BLACK"]
    else:
        num_pieces_left = 16 - state["captures"]["WHITE"]

    return 2 * (num_pieces_left) + random.random()


def offensive_eval_1(state, player):
    if player == "WHITE":
        num_pieces_left = 16 - state["captures"]["WHITE"]
    else:
        num_pieces_left = 16 - state["captures"]["BLACK"]
    
    return 2 * (32 - num_pieces_left) + random.random()


def defensive_eval_2(state, player):
    if player == "WHITE":
        num_my_pieces_left = 16 - state["captures"]["BLACK"]
        num_opp_pieces_left = 16 - state["captures"]["WHITE"]
        num_in_home_row = 0
        for col in state["board"][0]:
            if col == "WHITE":
                num_in_home_row += 1

    else:
        num_my_pieces_left = 16 - state["captures"]["WHITE"]
        num_opp_pieces_left = 16 - state["captures"]["BLACK"]
        num_in_home_row = 0
        for col in state["board"][7]:
            if col == "BLACK":
                num_in_home_row += 1

    return 2 * num_my_pieces_left + 3*num_in_home_row + random.random()

def offensive_eval_2(state, player):
    if player == "WHITE":
        num_my_pieces_left = 16 - state["captures"]["BLACK"]
        num_opp_pieces_left = 16 - state["captures"]["WHITE"]
        advance_score = 0
        win_score = 0
        near_score = 0

        for row in range(8):
            for col in range(8):
                if state["board"][row][col] == "WHITE":
                    # closer they are to black row, the higher the advance score
                    advance_score += (7 - row)

                if (state["board"][row][col] == "WHITE" and row == 0):
                    # white piece at row 0, best case
                    win_score += 1000
                if (state["board"][row][col] == "WHITE" and row == 1):
                    near_score += 25


    else:
        num_my_pieces_left = 16 - state["captures"]["WHITE"]
        num_opp_pieces_left = 16 - state["captures"]["BLACK"]
        win_score = 0
        advance_score = 0
        near_score = 0

        for row in range(8):
            for col in range(8):
                if state["board"][row][col] == "BLACK":
                    advance_score += row

                if (state["board"][row][col] == "BLACK" and row == 7):
                    win_score += 1000
                if (state["board"][row][col] == "WHITE" and row == 6):
                    near_score += 25


    return 6*(num_my_pieces_left - num_opp_pieces_left) + 4*advance_score + win_score + near_score + random.random()

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
    white_agent = MinimaxAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = MinimaxAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
