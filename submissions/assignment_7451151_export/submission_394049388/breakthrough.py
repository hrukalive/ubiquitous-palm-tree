import random
from copy import deepcopy
from tqdm import tqdm
from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.
"""
Part 1: This is the implemnation of the board it was already made for you 
by the professor. But quickly it is a 8x8 stored as a 2d list, and a state 
dictionary that is keeping track of captures and whose turn it is.
"""


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
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
        return state["to_move"]

    """
Part 2: This is the actions function that iterates through the board
and finds all valid moves for the current player. Allowing straight moves 
into empty places, and diagnal moves into empty spaces or captures.
    """

    def actions(self, state):
        ##########################################################################
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        moves = []
        player = self.to_move(state)
        board = state["board"]

        """
        Direction controlling row movement, it is always proper for color
        Opponinit is always properly set
        """
        direction = -1 if player == "WHITE" else 1
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    # Check diagnols and stragiht
                    for deltac in [-1, 0, 1]:
                        new_r = r + direction
                        new_c = c + deltac

                        # Check if move is on board still
                        if 0 <= new_r < 8 and 0 <= new_c < 8:
                            new_pos = board[new_r][new_c]

                            # Moving into spaces
                            # dc != 0, can move diagonal if empty or enemy
                            # dc == 0, can move only if empty
                            if deltac != 0:
                                if new_pos == "EMPTY" or new_pos == enemy:
                                    moves.append({"from": (r, c), "to": (new_r, new_c)})
                            else:
                                if new_pos == "EMPTY":
                                    moves.append({"from": (r, c), "to": (new_r, new_c)})
        return moves

    """
    Part 3: the result takes the action function and applies the moves. Using deepcopy
    to ensure that the original state is not modified. It moves the pieces and updates 
    captures accordingly, and then swaps the turn.
    """

    def result(self, state, action):

        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).

        new_state = deepcopy(state)
        board = new_state["board"]
        player = self.to_move(new_state)
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        from_r, from_c = action["from"]
        to_r, to_c = action["to"]

        # capture checking
        if board[to_r][to_c] == enemy:
            new_state["captures"][player] += 1

        # do move
        board[to_r][to_c] = player
        board[from_r][from_c] = "EMPTY"

        # swap turn
        new_state["to_move"] = enemy

        return new_state

    """
    Part 4: The utility function checks if the game is terminal,
      and if so returns a high positive value for a win, and a high 
      negative value for a loss. It checks for wins by seeing if any pieces have reached 
      the end of the board, or if either player has captured 16 pieces.
    """

    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

        if not self.terminal_test(state):
            return 0

        board = state["board"]

        # determine winner
        white_wins = "WHITE" in board[0] or state["captures"]["WHITE"] >= 16
        black_wins = "BLACK" in board[7] or state["captures"]["BLACK"] >= 16

        # postive = win, neg = loss
        if white_wins:
            return 1000 if player == "WHITE" else -1000
        elif black_wins:
            return 1000 if player == "BLACK" else -1000
        else:
            return 0

    """
    Part 5: The terminal test is checking if the game is over
    eitehr by a piece reaching the end of the board, or if all pieces 
    are captured.
    """

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]
        captures_w = state["captures"]["WHITE"]
        captures_b = state["captures"]["BLACK"]

        # piece reaches end of board
        if "WHITE" in board[0] or "BLACK" in board[7]:
            return True

        # all pieces captured
        if captures_w == 16 or captures_b == 16:
            return True

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


# Evaluation functions


def defensive_eval_1(state, player):
    enemy = "BLACK" if player == "WHITE" else "WHITE"
    number_pieces_remaining = 16 - state["captures"][enemy]
    return 2 * (number_pieces_remaining) + random.random()


def offensive_eval_1(state, player):
    enemy_pieces_remaining = 16 - state["captures"][player]
    return 2 * (32 - enemy_pieces_remaining) + random.random()


"""
Part 6:
For my custom defensive evaluation, I wanted to build on the basic defensive
hueristic by adding points to encourage the agent to keep pieces on the back row, 
My huersitic scans the back row and awards 2 points for each piece that is still on the back row
, which encourages the agent to keep pieces on the back row for defense. Valuing the 
back pieces more should encorage less offesnive movements making it a good defensive
hueristic. This should be better than teh basic hueristic because of the added encouragement
to keep pieces in the back row.
"""


def defensive_eval_2(state, player):
    base = defensive_eval_1(state, player)
    board = state["board"]
    backline_points = 0

    # determine back row
    back_row = 0 if player == "WHITE" else 7

    # check every back row and add points accordingly
    for c in range(8):
        if board[back_row][c] == player:
            backline_points += 2
    return base + backline_points


"""
Part 6 Continued:
For my custome offensive hueristic I wanted to encourage forward movement
my hueristic scans the entire board and finds how many rows forward the pieces are
and applies the bonus based off the distance forward. This should encourage aggressive 
behavior and forward movement. 

Move to breakthrough_agent.py
"""


def offensive_eval_2(state, player):
    base = offensive_eval_1(state, player)
    board = state["board"]
    bonus = 0

    # find all pieces and find how far forwar they are
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    distance = 7 - r
                else:
                    distance = r
                bonus += distance * 0.5
    return base + bonus


ag_eval_fn = (
    defensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
)
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
        "final_state": state,
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
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)
