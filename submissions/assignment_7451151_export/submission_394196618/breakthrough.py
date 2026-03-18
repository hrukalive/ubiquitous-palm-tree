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
        return state['to_move']

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
        actions = []

        player = state['to_move']

        directions = [(-1, -1), (0, -1), (1, -1)]  # for white
        if player == "BLACK":
            directions = [(d[0], d[1] * -1) for d in directions]

        border_x, border_y = len(state['board'][0]), len(state['board'])

        # For each player's piece...
        for r in range(border_y):
            for c in range(border_x):
                if state['board'][r][c] == player:
                    # Test each directional action
                    for dx, dy in directions:
                        x, y = c + dx, r + dy
                        if 0 <= x < border_x and 0 <= y < border_y:
                            # Cannot capture player's own pieces.
                            if state['board'][y][x] == player:
                                continue
                            # Cannot capture piece straight ahead
                            if dx !=0 or state['board'][y][x] == "EMPTY":
                                actions.append({
                                    "from": (r, c),
                                    "to": (y, x)}
                                )

        return actions

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
        from_y, from_x = action['from']
        to_y, to_x = action['to']

        player = state['to_move']
        opponent = "WHITE" if player == "BLACK" else "BLACK"

        # Move the player
        new_state['board'][to_y][to_x] = player
        new_state['board'][from_y][from_x] = "EMPTY"

        # If piece was captured, increase count
        if state['board'][to_y][to_x] == opponent:
            new_state['captures'][player] += 1

        new_state['to_move'] = opponent

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

        captured_white = state['captures']['WHITE'] == 16
        captured_black = state['captures']['BLACK'] == 16

        white_arrived = "WHITE" in state['board'][0]
        black_arrived = "BLACK" in state['board'][-1]

        if captured_white or black_arrived:
            return 1000 if player == "BLACK" else -1000
        if captured_black or white_arrived:
            return 1000 if player == "WHITE" else -1000

        return 0


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        return self.utility(state, state['to_move']) != 0



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
    player_pieces = 0
    height, width = len(state['board']), len(state['board'][0])

    for r in range(height):
        for c in range(width):
            if state['board'][r][c] == player:
                player_pieces += 1
    
    return 2 * player_pieces + random.random()


def offensive_eval_1(state, player):
    opp_pieces = 0
    height, width = len(state['board']), len(state['board'][0])

    for r in range(height):
        for c in range(width):
            if state['board'][r][c] not in ["EMPTY", player]:
                opp_pieces += 1

    return 2 * (32 - opp_pieces) + random.random()

def defensive_eval_2(state, player):
    protecting_pieces = 0
    backing_pieces = 0
    isolated_pieces = 0
    piece_difference = 0
    player_pieces = 0

    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_pieces = 0

    height, width = len(state['board']), len(state['board'][0])

    dy = -1 if player == "WHITE" else 1

    for r in range(height):
        for c in range(width):
            piece = state['board'][r][c]
            if piece == opponent:
                opp_pieces += 1
            if piece != player:
                continue

            player_pieces += 1

            if 0 <= r+(dy*-1) < height:
                # Find diagonally protecting pieces
                if c+1 < width and state['board'][r+(dy*-1)][c+1] == player:
                    protecting_pieces += 1
                if c-1 >= 0 and state['board'][r+(dy*-1)][c-1] == player:
                    protecting_pieces += 1

                # Find pieces backing another piece
                if state['board'][r+(dy*-1)][c] == player:
                    backing_pieces += 1

            # Find isolated pieces
            if c+1 < width and state['board'][r][c+1] != player \
                and c-1 >= 0 and state['board'][r][c-1] != player:
                isolated_pieces += 1

    piece_difference = player_pieces - opp_pieces

    return ((4 * piece_difference)
            + (3 * protecting_pieces)
            + (1 * backing_pieces)
            + (-4 * isolated_pieces)
            + random.random())

def offensive_eval_2(state, player):
    piece_difference = 0
    distance_traveled = 0
    threatening_pieces = 0

    player_pieces = 0
    opponent_pieces = 0

    opponent = "BLACK" if player == "WHITE" else "WHITE"

    height, width = len(state['board']), len(state['board'][0])

    dy = -1 if player == "WHITE" else 1

    for r in range(height):
        for c in range(width):
            piece = state['board'][r][c]
            if piece == opponent:
                opponent_pieces += 1
            if piece != player:
                continue
            player_pieces += 1

            # award pieces close to goal
            if player == "WHITE":
                distance_traveled += (height - 1) - r
            if player == "BLACK":
                distance_traveled += r

            if not (0 <= r+dy < height):
                continue
            # Find threatening pieces
            if c+1 < width and state['board'][r+dy][c+1] == opponent:
                threatening_pieces += 1
            if c-1 >= 0 and state['board'][r+dy][c-1] == opponent:
                threatening_pieces += 1

    piece_difference = player_pieces - opponent_pieces
    
    return ((4 * piece_difference)
            + (2 * distance_traveled)
            + (3 * threatening_pieces)
            + random.random())

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for competition.

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
        'final_board': state['board'],
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
    black_agent = AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
