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
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            "to_move": "WHITE",  # Player is also a string "WHITE" or "BLACK".
            "captures": {
                "WHITE": 0,
                "BLACK": 0,
            },  # Initially, white and black have captured 0 pieces.
            "board": grid,  # 8x8 grid representing the board.
        }  # ⚠️ You must use this structure for the state representation.

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
        # Return a dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }

        movements = []
        board = state["board"]
        rows = len(board)
        cols = len(board[0])
        if self.to_move(state) == "WHITE":  # whites moves
            for i in range(rows):
                for j in range(cols):
                    move = {"from": None, "to": None}
                    if board[i][j] == "WHITE":
                        if i > 0:
                            if (
                                board[i - 1][j] == "EMPTY"
                            ):  # check for forward movement
                                move["from"] = (i, j)
                                move["to"] = (i - 1, j)
                                movements.append(move.copy())
                            if (
                                j < cols - 1 and board[i - 1][j + 1] != "WHITE"
                            ):  # check for diagonal right move
                                move["from"] = (i, j)
                                move["to"] = (i - 1, j + 1)
                                movements.append(move.copy())
                            if (
                                j > 0 and board[i - 1][j - 1] != "WHITE"
                            ):  # check or diagonal left move
                                move["from"] = (i, j)
                                move["to"] = (i - 1, j - 1)
                                movements.append(move.copy())
        else:  # Black turn
            for i in range(rows):
                for j in range(cols):
                    move = {"from": None, "to": None}
                    if board[i][j] == "BLACK":
                        if i < rows - 1:
                            if (
                                board[i + 1][j] == "EMPTY"
                            ):  # check for forward movement
                                move["from"] = (i, j)
                                move["to"] = (i + 1, j)
                                movements.append(move.copy())
                            if (
                                j < cols - 1 and board[i + 1][j + 1] != "BLACK"
                            ):  # check for diagonal right move
                                move["from"] = (i, j)
                                move["to"] = (i + 1, j + 1)
                                movements.append(move.copy())
                            if (
                                j > 0 and board[i + 1][j - 1] != "BLACK"
                            ):  # check or diagonal left move
                                move["from"] = (i, j)
                                move["to"] = (i + 1, j - 1)
                                movements.append(move.copy())

        return movements

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
        nextState = deepcopy(state)
        board = nextState["board"]

        # move piece
        turn = self.to_move(state)
        if (
            turn == "WHITE"
            and nextState["board"][action["to"][0]][action["to"][1]] == "BLACK"
        ):  # increase capture count when capturing piece
            nextState["captures"]["WHITE"] += 1
        elif (
            turn == "BLACK"
            and nextState["board"][action["to"][0]][action["to"][1]] == "WHITE"
        ):
            nextState["captures"]["BLACK"] += 1

        nextState["board"][action["to"][0]][action["to"][1]] = turn
        nextState["board"][action["from"][0]][
            action["from"][1]
        ] = "EMPTY"  # empty players previous spot

        if turn == "WHITE":  # Swap players
            nextState["to_move"] = "BLACK"
        else:
            nextState["to_move"] = "WHITE"

        return nextState

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        # If the state is non-terminal there's no utility yet.
        # In a terminal state `state['to_move']` is the player who would move next
        # (i.e. the opponent of the player who just moved). Therefore to decide
        # who won we should look at the opposite of `to_move`.

        # The winner is the player who is NOT to move in the terminal state.
        winner = "WHITE" if self.to_move(state) == "BLACK" else "BLACK"
        if player == winner:
            return 1
        else:
            return -1

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        to_move = self.to_move(state)
        if (
            to_move
            == "WHITE"  # check depending on the term check if all the opponents pieces are missing
            and state["captures"]["BLACK"] == 16
        ) or (to_move == "BLACK" and state["captures"]["WHITE"] == 16):
            return True

        for i in range(
            len(state["board"][0])
        ):  # check the top and bottom row for the opposing piece
            if (
                state["board"][0][i] == "WHITE"
                or state["board"][len(state["board"]) - 1][i] == "BLACK"
            ):
                return True

        return False

    def display(self, state):
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print(
            "\n".join(
                "".join(chars[state["board"][r][c]] for c in range(8)) for r in range(8)
            )
        )
        if self.terminal_test(state):
            if self.to_move(state) == "WHITE":
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {state['to_move']}")
        print(
            f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces"
        )


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
        return (
            2 * (16 - state["captures"]["BLACK"]) + random.random()
        )  # use the capture number to konw the remaiing pieces
    return 2 * (16 - state["captures"]["WHITE"]) + random.random()


def offensive_eval_1(state, player):

    return 2 * (32 - (16 - state["captures"][player])) + random.random()


def defensive_eval_2(state, player):

    val = 0
    if player == "WHITE":
        val = (
            2 * (16 - state["captures"]["BLACK"]) + random.random()
        )  # use the capture number to konw the remaiing pieces
    else:
        val = 2 * (16 - state["captures"]["WHITE"]) + random.random()

    for i in range(8):  # check for pieces in the current players back row
        if player == "WHITE" and state["board"][7][i] == "WHITE":
            val += 2 + random.random()
        elif player == "BLACK" and state["board"][0][i] == "BLACK":
            val += 2 + random.random()

    return val


def offensive_eval_2(state, player):

    val = 3 * (32 - (16 - state["captures"][player])) + random.random()
    board = state["board"]

    offset = 1  #set offset so dont have to check for specific players
    if player == "WHITE":
        offset = -1

    for i in range(8):
        for j in range(8):

            if (
                board[i][j] == player
                and (j > 0 and board[i + offset][j - 1] == "EMPTY")
                and (j < 7 and board[i + offset][j + 1] == "EMPTY")
            ):  #check for pieces with safe diagonals
                val += 100 + random.random()

    return val


ag_eval_fn = (
    defensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
)

competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################


def play_game(
    white_agent, black_agent, max_moves=400, display=False, progress=False
):  # ⚠️ DO NOT CHANGE
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
    print(state)
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = (
            white_agent.select_move(game, state)
            if state["to_move"] == "WHITE"
            else black_agent.select_move(game, state)
        )
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
    white_time_per_move = sum(white_agent.time_per_move) / len(
        white_agent.time_per_move
    )
    black_time_per_move = sum(black_agent.time_per_move) / len(
        black_agent.time_per_move
    )
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state["captures"]["WHITE"]
    black_captures = state["captures"]["BLACK"]
    if display:
        game.display(state)
    return {
        "winner": (
            "white" if winner == "WHITE" else "black" if winner == "BLACK" else None
        ),
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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=defensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=offensive_eval_2)
    # white_agent = MinimaxAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    # black_agent = MinimaxAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)
