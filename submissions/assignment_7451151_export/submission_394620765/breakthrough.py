import random
# python's random model for tie-breaking
from copy import deepcopy

from tqdm import tqdm
# progress bar utility
from games import Game
#base abstract game class

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self):     # returns starting board state (do not change)
        # Initial state should look like Figure 1 in assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)] # creates 8x8 board filled with "empty"
        # loop and fill rows with 'black'
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK" # <-
        # loop & fill rows with 'white'
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        # to move -> white starts, board -> the 8x8 grid
        return {
            'to_move': "WHITE",                   # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0}, # Initially, white and black have captured 0 pieces.
            'board': grid,                        # 8x8 grid representing the board.
        } # ⚠️ You must use this structure for the state representation.

# method for whoever's turn it is currently
    def to_move(self, state):
        return state["to_move"]
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

    def _opponent(self, player):
        return "BLACK" if player == "WHITE" else "WHITE"

    def _in_bounds(self, r,c):
        return 0<= r < 8 and 0<= c < 8

    def actions(self, state): # returns all legal moves from current state

        player = self.to_move(state) #current player
        opponent = self._opponent(player) # is opponent black or white
        dr = -1 if player == "WHITE" else 1 #white moves up (-1), and black moves down (+1)
        board = state["board"] # reference local board
        moves = [] # collect legal moves as dict
        # loop over all cells and find pieces associated with curr player
        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue # and skip non-owned pieces
                rf= r + dr # forward row
                if self._in_bounds(rf, c) and board[rf][c]=="EMPTY":
                    moves.append({"from": (r,c), "to": (rf,c)})
                for dc in (-1, 1): # diagonally left & right
                    rd, cd = r + dr, c+dc
                    if self._in_bounds(rd, cd) and board[rd][cd] == opponent: #only diagonal captures are allowed
                        moves.append({"from": (r,c), "to": (rd,cd)})

        return moves


# Return a list of dict containing a "from" tuple and a "to" tuple for each
# legal move in this state.
# For example, to move a piece from (6,0) to (5,0), the action is
# represented as
# {
#     "from": (6,0),
#     "to": (5,0)
# }
# And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]

    def result(self, state, action):
        player = self.to_move(state)
        opponent = self._opponent(player)
        (r0, c0) = action["from"]
        (r1, c1) = action["to"]
        new_state = {
        "to_move": opponent,
        "captures": dict(state["captures"]),
        "board": deepcopy(state["board"]),
    }

        if new_state["board"][r1][c1] == opponent:
            new_state["captures"][player] += 1

        new_state["board"][r0][c0] = "EMPTY"
        new_state["board"][r1][c1] = player
        return new_state
                # Return the resulting state after applying the action to the current state.
            # The action is represented as a dict containing "to_move" (alternating),
            #      "captures" (updated captures) and "board" (updated grid).

    def utility(self, state, player):
        if not self.terminal_test(state):
            return 0
        winner = self._opponent(self.to_move(state))
        return 1 if winner == player else -1
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

    def terminal_test(self, state):
        board = state["board"]

        if "WHITE" in board[0] or "BLACK" in board[7]:
            return True
        white_count = 0
        black_count = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] =="WHITE":
                    white_count += 1
                elif board[r][c] =="BLACK":
                    black_count += 1
        if white_count == 0 or black_count == 0:
            return True

        if len(self.actions(state)) == 0:
            return True
                # Return True if this is a terminal state, False otherwise.
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

# Evaluation functions

def defensive_eval_1(state, player):
    own = sum(1 for r in range(8) for c in range(8)
              if state["board"][r][c] == player)
    return 2 * own + random.random()

def offensive_eval_1(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp = sum(1 for r in range(8) for c in range(8)
              if state["board"][r][c] == opponent)
    return 2 * (32- opp) + random.random()

def defensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state["board"]
    own_count = 0
    opp_count = 0
    own_home = 0
    own_under_attack = 0
    own_connections = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == player:
                own_count += 1

                if (player == "WHITE" and r == 7) or (player == "BLACK" and r == 0):
                    own_home += 1

                enemy_dr = 1 if player == "WHITE" else -1
                for dc in (-1, 1):
                    er, ec = r - enemy_dr, c + dc
                    if 0 <= er < 8 and 0 <= ec < 8 and board[er][ec] == opponent:
                        own_under_attack += 1
                        break

                if c + 1 < 8 and board[r][c + 1] == player:
                    own_connections += 1
                if r + 1 < 8 and board[r + 1][c] == player:
                    own_connections += 1
            elif piece == opponent:
                opp_count += 1

    return (
        7.0 * own_count
        - 5.0 * own_under_attack
        + 2.5 * own_home
        + 1.5 * own_connections
        - 1.5 * opp_count
        + random.random()
    )

def offensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state["board"]

    own_count = 0
    opp_count = 0
    advancement = 0
    capture_chances = 0
    almost_win = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == player:
                own_count += 1
                if player == "WHITE":
                    advancement += (7 - r)
                    tr = r - 1
                    if r == 1:
                        almost_win += 1
                else:
                    advancement += r
                    tr = r + 1
                    if r == 6:
                        almost_win += 1

                for dc in (-1, 1):
                    tc = c + dc
                    if 0 <= tr < 8 and 0 <= tc < 8 and board[tr][tc] == opponent:
                        capture_chances += 1
            elif piece == opponent:
                opp_count += 1

    return (
        6.0 * (16 - opp_count)
        + 1.2 * advancement
        + 4.5 * capture_chances
        + 8.0 * almost_win
        + 0.8 * own_count
        + random.random()
    )



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
