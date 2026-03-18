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
        player = state['to_move']
        board = state['board']

        dir = -1 if player == "WHITE" else 1

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    new_r = r + dir

                    if 0 <= new_r < 8 and board[new_r][c] == "EMPTY":
                        moves.append({"from": (r, c), "to": (new_r, c)})

                    new_c = c - 1
                    if 0 <= new_r < 8 and 0 <= new_c < 8:
                        target = board[new_r][new_c]
                        if target != player and target != "EMPTY":
                            moves.append({"from": (r, c), "to": (new_r, new_c)})

                    new_c = c + 1
                    if 0 <= new_r < 8 and 0 <= new_c < 8:
                        target = board[new_r][new_c]
                        if target != player and target != "EMPTY":
                            moves.append({"from": (r, c), "to": (new_r, new_c)})
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
        
        # Create a deep copy of the state to protect original
        new_state = deepcopy(state)

        from_pos = action["from"]
        to_pos = action["to"]
        from_r, from_c = from_pos
        to_r, to_c = to_pos

        player = new_state['to_move']
        board = new_state['board']

        # Check if a capture has occurred
        if board[to_r][to_c] != "EMPTY":
            new_state['captures'][player] += 1
        
        # Move the piece
        board[to_r][to_c] = player
        board[from_r][from_c] = "EMPTY"

        # Switch the player
        new_state['to_move'] = "BLACK" if player == "WHITE" else "WHITE"

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

        board = state['board']

        # Checks if either WHITE or BLACK has reached the opposite end of the board. If so, they've won
        for c in range(8):
            if board[0][c] == "WHITE":
                return 1 if player == "WHITE" else -1
            if board[7][c] == "BLACK":
                return 1 if player == "BLACK" else -1

        # Checks if either player has no pieces left. If so, the other player has won
        white_count = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        black_count = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")

        if white_count == 0:
            return 1 if player == "BLACK" else -1
        if black_count == 0:
            return 1 if player == "WHITE" else -1
        
        # Otherwise, return a non-terminal state
        return 0


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board = state['board']

        for c in range(8):
            if board[0][c] == "WHITE" or board[7][c] == "BLACK":
                return True
        
        white_count = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        black_count = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")
        if white_count == 0 or black_count == 0:
            return True
        
        if not self.actions(state):
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

def evals(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    # Count the number of pieces for both players
    p_cnt = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)
    o_cnt = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent)

    # Calculate the piece advantage
    piece_avtg = p_cnt - o_cnt

    # Advancement
    if player == "WHITE":
        p_adv = sum(7 - r for r in range(8) for c in range(8) if board[r][c] == player)
        o_adv = sum(r for r in range(8) for c in range(8) if board[r][c] == opponent)
    else:
        p_adv = sum(r for r in range(8) for c in range(8) if board[r][c] == player)
        o_adv = sum(7 - r for r in range(8) for c in range(8) if board[r][c] == opponent)

    # Captures
    cap = state['captures'][player] - state['captures'][opponent]
    
    return piece_avtg, p_adv, o_adv, cap

def defensive_eval_1(state, player):
    piece_avtg, p_adv, o_adv, cap = evals(state, player)

    # Weighted Eval
    ## Numbers are arbitrary for now
    eval = (piece_avtg * 10 + (p_adv - o_adv) * 5 + cap * 8)

    return eval


def offensive_eval_1(state, player):
    piece_avtg, p_adv, o_adv, cap = evals(state, player)

    # Weighted Eval
    ## Numbers are arbitrary for now
    eval = (piece_avtg * 5 + (p_adv - o_adv) * 2 + cap * 12)
    
    return eval


def defensive_eval_2(state, player):
    piece_avtg, p_adv, o_adv, cap = evals(state, player)

    # Add penalties
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    if player == "WHITE":
        o_thrt = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent and r < 6)
    else:
        o_thrt = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent and r > 1)

    # Weighted Eval
    ## Numbers are arbitrary for now
    eval = (piece_avtg * 15 + (p_adv - o_adv) * 4 - o_thrt * 20 + cap * 5)
    
    return eval


def offensive_eval_2(state, player):
    piece_avtg, p_adv, o_adv, cap = evals(state, player)

    # Add bonuses
    board = state['board']

    if player == "WHITE":
        p_adv_sq = sum((7 - r) ** 2 for r in range(8) for c in range(8) if board[r][c] == player)
        o_adv_sq = sum(r ** 2 for r in range(8) for c in range(8) if board[r][c] == "BLACK")
    else:
        p_adv_sq = sum(r ** 2 for r in range(8) for c in range(8) if board[r][c] == player)
        o_adv_sq = sum((7 - r) ** 2 for r in range(8) for c in range(8) if board[r][c] == "WHITE")

    # Weighted Eval
    ## Numbers are arbitrary for now
    eval = (piece_avtg * 3 + (p_adv_sq - o_adv_sq) * 2 + cap * 18)
    
    return eval

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
