import random
from functools import lru_cache

from tqdm import tqdm
from frozendict import frozendict
# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class IllegalActionError(Exception):
    pass


EMPTY, WHITE, BLACK = 0, 1, 2

def is_empty(rows, r: int, c: int) -> bool:
    b, w = rows[r]
    return ((b | w) & (1 << c)) == 0

def color_at(rows, r: int, c: int):
    b, w = rows[r]
    m = 1 << c
    if b & m:
        return BLACK
    if w & m:
        return WHITE
    return None  # empty

def has_color(rows, r: int, c: int, color: str) -> bool:
    b, w = rows[r]
    m = 1 << c
    return (b & m) != 0 if color == BLACK else (w & m) != 0

class Breakthrough:
    @staticmethod
    def initial_state(): # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        board = (
            # BLACK, WHITE
            (0b11111111, 0),  # row 0
            (0b11111111, 0),  # row 1
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0b11111111),
            (0, 0b11111111),
        )
        # board, to move, white captures, black captures
        return (board, WHITE, 0, 0)
    
    @staticmethod
    def to_move(state):
        return state[1]

    @staticmethod
    def actions(state):
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
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        return Breakthrough._legal_moves(state[0], state[1])

    @staticmethod
    @lru_cache(maxsize=10000)
    def result(state, action):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a tuple containing "from" and "to" positions.
        #      "to_move" (alternating), "captures" (updated captures),
        #      and "board" (updated grid).
        board, player, wc, bc = state
        legal_moves = Breakthrough._legal_moves(board, player)
        if action not in legal_moves:
            raise IllegalActionError
        (r, c), (nr, nc) = action[0], action[1]

        if not has_color(board, r, c, player):
            Breakthrough.display(state)
            print(action)
            raise IllegalActionError
        dest_color = color_at(board, nr, nc)
        if dest_color == player:
            raise IllegalActionError
        if abs(nr - r) != 1 or abs(nc - c) > 1:
            raise IllegalActionError

        captured = (dest_color is not None and dest_color != player)

        rows = list(board)
        b0, w0 = rows[r]
        b1, w1 = rows[nr]
        m0 = 1 << c
        m1 = 1 << nc
        if player == BLACK:
            # remove source black bit
            b0 &= ~m0
            # capture: clear dest from white
            w1 &= ~m1
            # place black at dest
            b1 |= m1
        else:
            w0 &= ~m0
            b1 &= ~m1
            w1 |= m1
        rows[r]  = (b0 & 0xFF, w0 & 0xFF)
        rows[nr] = (b1 & 0xFF, w1 & 0xFF)
        new_board = tuple(rows)

        if captured:
            if player == WHITE:
                wc += 1
            else:
                bc += 1
        return (new_board, WHITE if player == BLACK else BLACK, wc, bc)

    @staticmethod
    def utility(state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if Breakthrough.terminal_test(state):
            if state[1] == player:
                return -500000
            else:
                return 500000
        return 0

    @staticmethod
    @lru_cache(maxsize=10000)
    def terminal_test(state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        board, player, wc, bc = state
        if board[0][1] != 0:
            return True
        if board[7][0] != 0:
            return True
        white_exists = (16 - bc) > 0
        black_exists = (16 - wc) > 0
        if not white_exists or not black_exists:
            return True
        if not Breakthrough._any_legal_moves(board, player):
            return True
        return False

    @staticmethod
    @lru_cache(maxsize=1024)
    def display(state):
        board, player, wc, bc = state
        for r in range(8):
            bmask, wmask = board[r]
            line = []
            for c in range(8):
                m = 1 << c
                if wmask & m:
                    line.append("W")
                elif bmask & m:
                    line.append("B")
                else:
                    line.append(".")
            print("".join(line))
        if Breakthrough.terminal_test(state):
            if player == WHITE:
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {'WHITE' if player == WHITE else 'BLACK'}")
        print(f"Captures: White captured {wc} pieces, Black captured {bc} pieces")

    @staticmethod
    @lru_cache(maxsize=10000)
    def _legal_moves(board, player):
        d = -1 if player == WHITE else 1
        moves = []
        for r in range(8):
            mask = board[r][1] if player == WHITE else board[r][0]
            if mask == 0:
                continue

            # iterate set bits (columns with player's pieces)
            m = mask & 0xFF
            while m:
                lsb = m & -m
                c = (lsb.bit_length() - 1)
                m &= m - 1

                nr = r + d
                if not (0 <= nr < 8):
                    continue

                # forward (must be empty)
                if is_empty(board, nr, c):
                    moves.append(((r, c), (nr, c)))

                # diagonals: allowed if empty OR occupied by opponent (same as your original)
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < 8:
                        dest = color_at(board, nr, nc)
                        if dest != player:  # empty or opponent
                            moves.append(((r, c), (nr, nc)))
        if player == WHITE:
            moves.sort(key=lambda move: move[0], reverse=False)
        else:
            moves.sort(key=lambda move: move[0], reverse=True)
        return moves

    @staticmethod
    @lru_cache(maxsize=10000)
    def _any_legal_moves(board, player):
        d = -1 if player == WHITE else 1
        for r in range(8):
            mask = board[r][1] if player == WHITE else board[r][0]
            if mask == 0:
                continue
            # iterate set bits (columns with player's pieces)
            m = mask & 0xFF
            while m:
                lsb = m & -m
                c = (lsb.bit_length() - 1)
                m &= m - 1

                nr = r + d
                if not (0 <= nr < 8):
                    continue

                # forward (must be empty)
                if is_empty(board, nr, c):
                    return True

                # diagonals: allowed if empty OR occupied by opponent (same as your original)
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < 8:
                        dest = color_at(board, nr, nc)
                        if dest != player:  # empty or opponent
                            return True
        return False


    @staticmethod
    @lru_cache(maxsize=10000)
    def bitboard_to_state(state) -> dict:
        board, player, wc, bc = state
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]

        for r in range(8):
            bmask, wmask = board[r]
            # Optional sanity check: no overlap
            if (bmask & wmask) != 0:
                raise ValueError(f"Invalid bitboard: overlap at row {r}")

            for c in range(8):
                m = 1 << c
                if bmask & m:
                    grid[r][c] = "BLACK"
                elif wmask & m:
                    grid[r][c] = "WHITE"

        return frozendict({
            "to_move": "WHITE" if player == WHITE else "BLACK",
            "captures": frozendict({"WHITE": wc, "BLACK": bc}),
            "board": tuple(map(tuple, grid)),
        })

##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

@lru_cache(maxsize=10000)
def defensive_eval_1(state, player):
    wc = 16 - state["captures"]["WHITE"]  # white pieces remaining
    bc = 16 - state["captures"]["BLACK"]  # black pieces remaining
    own = wc if player == "WHITE" else bc
    return 2 * own + random.random()


@lru_cache(maxsize=10000)
def offensive_eval_1(state, player):
    wc = 16 - state["captures"]["WHITE"]  # white pieces remaining
    bc = 16 - state["captures"]["BLACK"]  # black pieces remaining
    opp = bc if player == "WHITE" else wc
    return 2 * (30 - opp) + random.random()


@lru_cache(maxsize=10000)
def defensive_eval_2(state, player):
    return defensive_eval_1(state, player)


@lru_cache(maxsize=10000)
def offensive_eval_2(state, player):
    return offensive_eval_1(state, player)

ag_eval_fn = defensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ You may change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, display_final=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.

    :param white_agent: An agent that plays white.
    :param black_agent: An agent that plays black.
    :param max_moves: The maximum number of moves to play.
    :param display: Whether to display the game state during play.
    :param display_final: Whether to display the final game state.
    :param progress: Whether to show a progress bar.
    :return: The statistic of the game play.
    """
    game = Breakthrough()

    state = game.initial_state()
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = white_agent.select_move(game, state) if state[1] == WHITE else black_agent.select_move(game, state)
        state = game.result(state, move)
        if display:
            game.display(state)
        move_count += 1
        if progress:
            pbar.update()
        if game.terminal_test(state):
            winner = WHITE if state[1] == BLACK else BLACK
            break
        if move_count >= max_moves:
            winner = None
            raise TimeoutError(f"Game exceeded max moves ({max_moves}), declaring draw")
    if progress:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = (sum(white_agent.time_per_move) / len(white_agent.time_per_move))
    black_time_per_move = (sum(black_agent.time_per_move) / len(black_agent.time_per_move))
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state[2]
    black_captures = state[3]
    if display or display_final:
        game.display(state)
    return {
        'final_state': state,
        'winner': 'white' if winner == WHITE else ('black' if winner == BLACK else None),
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
    from breakthrough_agent_internal import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=3, display=True, progress=True)
    print(results)
