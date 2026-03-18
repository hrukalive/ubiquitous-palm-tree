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
        return state["to_move"]
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

    def actions(self, state):
        grid = state["board"]
        action = []
        player = state["to_move"]
        directions = {"BLACK":[(1,0),(1,1), (1,-1)], "WHITE": [(-1,0), (-1,1), (-1,-1)]}
        for r in range(8):
            for c in range(8):
                if grid[r][c] == player:
                    for dir_row, dir_col in directions[grid[r][c]]:
                        next_row, next_col = r + dir_row, c + dir_col
                        if 0 <= next_row < 8 and 0 <= next_col < 8:
                            if dir_col == 0:
                                if grid[next_row][next_col] == "EMPTY":
                                    action.append({"from": (r, c), "to":(next_row, next_col)})
                            else:
                                if grid[r][c] == "BLACK" and grid[next_row][next_col] != "BLACK":
                                    action.append({"from": (r, c), "to": (next_row, next_col)})
                                if grid[r][c] == "WHITE" and grid[next_row][next_col] != "WHITE":
                                    action.append({"from": (r, c), "to": (next_row, next_col)})
        return action






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

    def result(self, state, action):
        r,c = action["to"]
        old_r, old_c = action["from"]
        player = state["to_move"]
        new_grid = deepcopy(state["board"])
        new_grid[r][c] = player
        new_grid[old_r][old_c] = "EMPTY"
        black_captures = state["captures"]["BLACK"]
        white_captures = state["captures"]["WHITE"]
        if state["board"][r][c] == "BLACK" and player == "WHITE":
            white_captures += 1
        if state["board"][r][c] == "WHITE" and player == "BLACK":
            black_captures += 1
        return {
            "to_move":"WHITE" if player == "BLACK" else "BLACK",
            "captures":{"WHITE": white_captures, "BLACK": black_captures},
            "board": new_grid
        }
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).


    def utility(self, state, player):
        grid = state["board"]
        black_home = grid[7]
        white_home = grid[0]
        black_captures = state["captures"]["BLACK"]
        white_captures = state ["captures"]["WHITE"]
        if "BLACK" in black_home:
            return 1 if player == "BLACK" else -1
        if "WHITE" in white_home:
            return 1 if player == "WHITE" else -1
        if black_captures == 16:
            return 1 if player == "BLACK" else -1
        if white_captures == 16:
            return 1 if player == "WHITE" else -1
        return 0
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.


    def terminal_test(self, state):
        grid = state["board"]
        black_home = grid[7]
        white_home = grid[0]
        black_captures = state["captures"]["BLACK"]
        white_captures = state["captures"]["WHITE"]
        return "BLACK" in black_home or "WHITE" in white_home or black_captures == 16 or white_captures == 16
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.


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
    if player == "BLACK":
        own_pieces = 16 - state["captures"]["WHITE"]
    if player == "WHITE":
        own_pieces = 16 - state["captures"]["BLACK"]

    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    if player == "BLACK":
        opponent = 16 - state["captures"]["BLACK"]
    if player == "WHITE":
        opponent = 16 - state["captures"]["WHITE"]
    
    return 2 * (32 - opponent) + random.random()


def defensive_eval_2(state, player):
    grid = state["board"]
    black_blocks = 0
    white_blocks = 0
    safe_black = 0
    safe_white = 0
    for r in range(8):
        for c in range(8):
            if grid[r][c] == "BLACK":
                if grid[r+1][c] == "WHITE" and (c == 0 or grid[r+1][c-1] == "BLACK") and (c == 7 or grid[r+1][c+1] == "BLACK"):
                    white_blocks +=1
                if r != 0 and (c == 0 or grid[r-1][c-1] == "BLACK") and (c == 7 or grid[r-1][c+1] == "BLACK"):
                    safe_black +=1
            if grid[r][c] == "WHITE":
                if grid[r - 1][c] == "BLACK" and (c == 0 or grid[r-1][c-1] == "WHITE") and (c == 7 or grid[r-1][c+1] == "WHITE"):
                    black_blocks += 1
                if r != 7 and (c == 0 or grid[r+1][c-1] == "WHITE") and (c == 7 or grid[r+1][c+1] == "WHITE"):
                    safe_white +=1
    if player == "WHITE":
        player_blocks = white_blocks
        player_pieces = 16 - state["captures"]["BLACK"]
        opponent = 16 - state["captures"]["WHITE"]
        safe_player = safe_white
    if player == "BLACK":
        player_blocks = black_blocks
        player_pieces = 16 - state["captures"]["BLACK"]
        opponent = 16 - state["captures"]["WHITE"]
        safe_player = safe_black
    return .1*(player_pieces - opponent) + .4*(safe_player)  + .5*(player_blocks) + random.random()


def offensive_eval_2(state, player):
    grid = state["board"]
    total_black_distance = 0
    total_white_distance = 0
    black_threat = 0
    white_threat = 0
    for r in range(8):
        for c in range(8):
            if grid[r][c] == "BLACK":
                total_black_distance += r - 0
                if r == 6:
                    black_threat +=2
                if r != 7:
                    if r + 1 == "EMPTY" and (c != 0 and grid[r+1][c-1] == "EMPTY") and (c != 7 and grid[r+1][c+1] == "EMPTY"):
                        black_threat+=.5
                    if (c != 0 and grid[r+1][c-1] == "WHITE") or (c != 7 and grid[r+1][c+1] == "WHITE"):
                        black_threat +=1
            if grid[r][c] == "WHITE":
                total_white_distance += 7 - r
                if r == 1:
                    white_threat +=2
                if r != 0:
                    if r - 1 == "EMPTY" and (c == 0 or grid[r - 1][c - 1] == "EMPTY") and (
                        c == 7 or grid[r - 1][c + 1] == "EMPTY"):
                        white_threat += .5
                        if (c != 0 and grid[r - 1][c - 1] == "BLACK") or (c != 7 and grid[r - 1][c + 1] == "BLACK"):
                            white_threat += 1
    if player == "BLACK":
        player_threats = black_threat
        player_distance = total_black_distance
        player_pieces = 16 - state["captures"]["BLACK"]
        opponent = 16 - state["captures"]["WHITE"]
    if player == "WHITE":
        player_threats = white_threat
        player_distance = total_white_distance
        player_pieces = 16 - state["captures"]["BLACK"]
        opponent = 16 - state["captures"]["WHITE"]
    return .1*(player_pieces - opponent) + .4*(player_distance) + .5 *(player_threats) + random.random()

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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_2)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
