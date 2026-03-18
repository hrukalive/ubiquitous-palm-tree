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
        board = state["board"]
        whose_move = state["to_move"]

        # Decides displacement, up or down, for the row, depending on which player's turn it is
        if whose_move == "WHITE":
            dr = -1
            opponent = "BLACK"
        else:
            dr = 1
            opponent = "WHITE"

        # Iterate across the board, finding workers belonging to the player whose turn it is, 
        # and appending their legal moves
        for r in range(8):
            for c in range(8):
                if board[r][c] == whose_move:
                    new_r = r + dr
                    # Forward: must be empty
                    if 0 <= new_r < 8:
                        if board[new_r][c] == "EMPTY":
                            moves.append({
                                "from": (r, c),
                                "to": (new_r, c)
                            })
                    # Diagonal left: must be an enemy worker there to capture
                    new_c = c - 1
                    if 0 <= new_r < 8 and 0 <= new_c < 8:
                        if board[new_r][new_c] == opponent:
                            moves.append({
                                "from": (r, c),
                                "to": (new_r, new_c)
                            })
                    # Diagonal right: must be an enemy worker there to capture
                    new_c = c + 1
                    if 0 <= new_r < 8 and 0 <= new_c < 8:
                        if board[new_r][new_c] == opponent:
                            moves.append({
                                "from": (r, c),
                                "to": (new_r, new_c)
                            })
        return moves


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
        board = new_state["board"]
        from_r, from_c = action["from"]
        to_r, to_c = action["to"]
        # Origin square and destination square assignment
        from_sqr = board[from_r][from_c]
        to_sqr = board[to_r][to_c]

        # Updates piece placement on board
        board[from_r][from_c] = "EMPTY"
        board[to_r][to_c] = from_sqr

        # If a piece is in the new square, capture it
        if to_sqr != "EMPTY":
            new_state["captures"][from_sqr] += 1

        # Swap whose turn it is
        if from_sqr == "WHITE":
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
        board = state["board"]

        # If a player has no legal moves, the other player wins
        if len(self.actions(state)) == 0:
            if state["to_move"] == player:
                # Wins/losses return large-magnitude integers so that normal moves
                # cannot be seen as more/less desirable than a win/loss
                return -1000
            else:
                return 1000

        # If player 1 captures all of player 2's pieces, player 1 wins
        if state["captures"]["WHITE"] == 16:
            winner = "WHITE"
            if player == winner:
                return 1000
            else:
                return -1000
        if state["captures"]["BLACK"] == 16:
            winner = "BLACK"
            if player == winner:
                return 1000
            else:
                return -1000
        
        # If a player has reached the opposite side of the board, that player wins
        for c in range(8):
            if board[0][c] == "WHITE":
                winner = "WHITE"
                if player == winner:
                    return 1000
                else:
                    return -1000
            if board[7][c] == "BLACK":
                winner = "BLACK"
                if player == winner:
                    return 1000
                else:
                    return -1000
        return 0


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]

        # If a player has no legal moves, the other player wins
        if len(self.actions(state)) == 0:
            return True
        
        # If player 1 captures all of player 2's pieces, player 1 wins
        if state["captures"]["WHITE"] == 16:
            return True
        if state["captures"]["BLACK"] == 16:
            return True
        
        # If a player has reached the opposite side of the board, that player wins
        for c in range(8):
            if board[0][c] == "WHITE":
                return True
            if board[7][c] == "BLACK":
                return True
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



##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    # 2 * (number_of_own_pieces_remaining) + random()
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    num_pieces = 16 - state["captures"][opponent]
    return 2 * num_pieces + random.random()


def offensive_eval_1(state, player):
    # 2 * (32 - number_of_opponent_pieces_remaining) + random()
    # Same as:
    # 2 * (32 - (16 - player_captures)) + random()
    # Same as:
    # 2 * (16 + player_captures) + random()
    return 2 * (16 + state["captures"][player]) + random.random()


def defensive_eval_2(state, player):
    board = state["board"]
    score = 0
    player_count = 0
    opponent_progress = 0
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"

    # Iterate across the board, finding all pieces and evaluating the player's
    # score for each move based off piece placement
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                # Rewards 1 for all the player's pieces still on the board
                player_count += 1
            elif board[r][c] == opponent:
                # Penalizes opponent advacement
                if opponent == "WHITE":
                    # i.e. white opponent going up the board
                    opponent_progress += (7 - r)
                else:
                    # i.e. black opponent going down the board
                    opponent_progress += r
    # Weight of 4 is used to make preserving pieces more relevant
    score += 4 * player_count
    # Weight of 3 makes each piece's advancement more relevant
    score -= 3 * opponent_progress
    return score + random.random()


def offensive_eval_2(state, player):
    board = state["board"]
    score = 0
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"

    # Iterate across the board, finding all pieces and evaluating the player's
    # score for each move based off piece placement
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    # Rewards the player's (playing white) advancement
                    # i.e. going up the board
                    score += (7 - r)
                else:
                    # Rewards the player's (playing black) advancement
                    # i.e. going down the board
                    score += r
            elif board[r][c] == opponent:
                if opponent == "WHITE":
                    # Penalizes the opponent's (playing white) advancement
                    # i.e. going up the board
                    score -= (7 - r)
                else:
                    # Penalizes the opponent's (playing black) advancement
                    # i.e. going down the board
                    score -= r
    # Weight of 5 heavily encourages captures, good for offense
    score += 5 * state["captures"][player]
    return score + random.random()


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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
