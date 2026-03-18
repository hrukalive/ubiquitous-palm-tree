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


    # ________________________________________ to_move ________________________________________
    # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
    def to_move(self, state):
        return state['to_move']

    # ________________________________________ actions ________________________________________
    # Return a list of dict containing a "from" tuple and a "to" tuple for each
    # legal move in this state.
    # For example, to move a piece from (6,0) to (5,0), the action is
    # represented as
    # {
    #     "from": (6,0),
    #     "to": (5,0)
    # }
    # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
    def actions(self, state):
        # create a hashset for each team's pieces
        white_pieces = set()
        black_pieces = set()

        for r in range(0, 8):
            for c in range(0, 8):
                if state['board'][r][c] == "WHITE":
                    white_pieces.add((r, c))
                if state['board'][r][c] == "BLACK":
                    black_pieces.add((r, c))


        # decide who is friendly / opponent and row direction by to_move
        to_move = state['to_move']
        if to_move == "WHITE":
            pieces = white_pieces
            opponent_pieces = black_pieces
            row_move = -1
        else:
            pieces = black_pieces
            opponent_pieces = white_pieces
            row_move = 1

        # for each piece, evaluate the possible moves
        moves = []
        for (r, c) in pieces:
            # can move forward if space is empty
            if (r+row_move, c) not in opponent_pieces and (r+row_move, c) not in pieces:
                moves.append({"from":(r,c), "to":(r+row_move, c)})

            # can move diagonal if space is not occupied by friendly or edge
            if c-1 >= 0 and (r+row_move, c-1) not in pieces:
                moves.append({"from": (r, c), "to": (r + row_move, c-1)})
            if c+1 <= 7 and (r+row_move, c+1) not in pieces:
                moves.append({"from": (r, c), "to": (r + row_move, c+1)})

        return moves


    # ________________________________________ result ________________________________________
    # Return the resulting state after applying the action to the current state.
    # The action is represented as a dict containing "to_move" (alternating),
    #      "captures" (updated captures) and "board" (updated grid).
    def result(self, state, action):
        board = deepcopy(state['board'])
        r1, c1 = action["from"]
        r2, c2 = action["to"]

        # update captures if need be
        captures = state['captures'].copy()
        if board[r2][c2] == "WHITE": captures["BLACK"] += 1
        elif board[r2][c2] == "BLACK": captures["WHITE"] += 1

        # update the to and from squares on the board
        board[r2][c2] = board[r1][c1]
        board[r1][c1] = "EMPTY"

        # update the to_move
        to_move = ""
        if state['to_move'] == "WHITE": to_move = "BLACK"
        else: to_move = "WHITE"

        return {'to_move': to_move, 'captures': captures, 'board': board}

    # ________________________________________ utility ________________________________________
    # Return the value to the perspective of the "player";
    #    Positive for win, negative for loss, 0 otherwise.
    def utility(self, state, player):
        winner = None
        captures = state['captures']
        if captures['WHITE'] == 16: winner = "WHITE"
        elif captures['BLACK'] == 16: winner = "BLACK"

        else:
            for c in range(0, 8):
                if state['board'][0][c] == "WHITE":
                    winner = "WHITE"
                    break
                if state['board'][7][c] == "BLACK":
                    winner = "BLACK"
                    break

        if winner == player:
            return 9999
        elif winner is not None:
            return -9999
        return 0

    # ________________________________________ terminal_test ________________________________________
    # Return True if this is a terminal state, False otherwise.
    def terminal_test(self, state):

        # if either team runs out of pieces
        captures = state['captures']
        if captures['WHITE'] == 16 or captures['BLACK'] == 16:
            return True

        # if either team reaches the end
        for c in range(0, 8):
            if state['board'][0][c] == "WHITE" or state['board'][7][c] == "BLACK":
                return True

        return False

    # ________________________________________ display ________________________________________
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



# ======================================== Evaluation functions ========================================
# ________________________________________ defensive_eval_1 ________________________________________
def defensive_eval_1(state, player):
    # 2 * (number_of_own_pieces_remaining) + random()
    if player == "WHITE": opponent = "BLACK"
    else: opponent = "WHITE"

    return 2 * (16 - state['captures'][opponent]) + random.random()


# ________________________________________ offensive_eval_2 ________________________________________
def offensive_eval_1(state, player):
    # 2 * (32 - number_of_opponent_pieces_remaining ) + random()
    # (32 - (16 - captures)) = (16 + captures)
    return 2 * (16 + state['captures'][player]) + random.random()


# ________________________________________ defensive_eval_2 ________________________________________
def defensive_eval_2(state, player):
    val = 0
    board = state['board']

    # search for player's pieces
    for r in range(0, 8):
        for c in range(0, 8):
            if board[r][c] == player:
                val += 10 # each piece left is added value

                # staying back is good (add value)
                if player == "WHITE" and r > 5:
                    val += 5
                if player == "BLACK" and r < 2:
                    val += 5

                # having friends is good
                # horizontal lines create protection from capture
                if c < 7 and board[r][c+1] == player:
                    val += 5
                if c == 7 and board[r][c-1] == player:
                    val += 5

                # diagonal back pieces provide retaliation and further prevention
                if r > 0 and c > 0 and board[r-1][c-1] == player:
                    val += 5
                if r > 0 and c < 7 and board[r-1][c+1] == player:
                    val += 5

    return val + random.random()


# ________________________________________ offensive_eval_2 ________________________________________
def offensive_eval_2(state, player):
    val = 0
    board = state['board']

    # search for player's pieces
    for r in range(0, 8):
        for c in range(0, 8):
            if board[r][c] == player:
                if player == "WHITE":
                    distance = 7-r
                else:
                    distance = r
                # points based on progress to the opposite edge, not just being alive. exponential reward
                val += (distance **2)

                # extra bonus for one move away
                if distance == 6:
                    val += 50
    # also prioritizes captures
    val += (state['captures'][player] * 12)

    return val + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
