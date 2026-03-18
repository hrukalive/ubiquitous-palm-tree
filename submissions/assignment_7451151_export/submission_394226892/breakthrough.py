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
        """Return the player whose turn it is."""
        return state["to_move"]

    def actions(self, state):
        """Return a list of legal moves for the current player.

        Each action is a dict: {"from": (r1, c1), "to": (r2, c2)}.
        Rows are 0..7 from top to bottom.
        """
        board = state["board"]
        player = state["to_move"]
        enemy = "BLACK" if player == "WHITE" else "WHITE"
        dr = -1 if player == "WHITE" else 1  # White moves up (toward row 0); Black moves down.

        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                r2 = r + dr
                if not (0 <= r2 < 8):
                    continue

                # Forward
                if board[r2][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (r2, c)})

                # Diagonal left/right (move or capture)
                for dc in (-1, 1):
                    c2 = c + dc
                    if not (0 <= c2 < 8):
                        continue
                    target = board[r2][c2]
                    if target == "EMPTY" or target == enemy:
                        moves.append({"from": (r, c), "to": (r2, c2)})

        return moves

    def result(self, state, action):
        """Apply action and return a NEW state (does not mutate input state)."""
        new_state = {
            "to_move": "BLACK" if state["to_move"] == "WHITE" else "WHITE",
            "captures": deepcopy(state["captures"]),
            "board": deepcopy(state["board"]),
        }

        (r1, c1) = action["from"]
        (r2, c2) = action["to"]

        player = state["to_move"]
        enemy = "BLACK" if player == "WHITE" else "WHITE"

        # Handle capture (diagonal into enemy piece)
        if new_state["board"][r2][c2] == enemy:
            new_state["captures"][player] += 1

        new_state["board"][r2][c2] = player
        new_state["board"][r1][c1] = "EMPTY"
        return new_state



    def utility(self, state, player):
        """Utility is from the perspective of `player`.

        Terminal win = +1, terminal loss = -1, otherwise 0.
        """
        if not self.terminal_test(state):
            return 0

        # Winner is the player who made the last move (opposite of state["to_move"]).
        winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
        return 1 if winner == player else -1



    def terminal_test(self, state):
        board = state["board"]

        # Home-base reach: White reaches row 0, Black reaches row 7.
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True

        # Elimination: one side has no pieces.
        white_left = sum(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_left = sum(board[r][c] == "BLACK" for r in range(8) for c in range(8))
        if white_left == 0 or black_left == 0:
            return True

        # Rare: no legal moves for side to move -> treat as terminal (side to move loses).
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
# Evaluation functions
#
# All eval functions return a value from the perspective of `player`.
# Larger is better for `player`. They are only used at depth cutoffs.

def _opponent(player: str) -> str:
    return "BLACK" if player == "WHITE" else "WHITE"


def _count_pieces(board, who: str) -> int:
    return sum(board[r][c] == who for r in range(8) for c in range(8))


def _advancement_score(board, player: str) -> int:
    """Sum of how many rows each piece has advanced toward the goal."""
    score = 0
    if player == "WHITE":
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    score += (7 - r)  # 0 at home row (7), 7 at goal row (0)
    else:
        for r in range(8):
            for c in range(8):
                if board[r][c] == "BLACK":
                    score += r  # 0 at home row (0), 7 at goal row (7)
    return score


def _pieces_under_attack(board, player: str) -> int:
    """Count of player's pieces that can be captured on opponent's next move."""
    opp = _opponent(player)
    threatened = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue
            # An enemy piece one row behind diagonally can capture this.
            if player == "WHITE":
                rr = r - 1  # black moves down, so black would be at r-1 to capture to r
                for dc in (-1, 1):
                    cc = c + dc
                    if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == opp:
                        threatened += 1
                        break
            else:
                rr = r + 1  # white moves up, so white would be at r+1 to capture down to r
                for dc in (-1, 1):
                    cc = c + dc
                    if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == opp:
                        threatened += 1
                        break
    return threatened


def _almost_win(board, player: str) -> int:
    """Pieces on the enemy's 2nd-farthest row (one step from winning)."""
    target_row = 1 if player == "WHITE" else 6
    return sum(board[target_row][c] == player for c in range(8))


def _home_row_pieces(board, player: str) -> int:
    row = 7 if player == "WHITE" else 0
    return sum(board[row][c] == player for c in range(8))


def _connected_pairs(board, player: str) -> int:
    """Count adjacent friendly pairs (horizontal + vertical)."""
    pairs = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue
            if c + 1 < 8 and board[r][c + 1] == player:
                pairs += 1
            if r + 1 < 8 and board[r + 1][c] == player:
                pairs += 1
    return pairs


def defensive_eval_1(state, player):
    """Dummy defensive eval from the spec: more own pieces = better (plus noise)."""
    board = state["board"]
    own = _count_pieces(board, player)
    return 2 * own + random.random()


def offensive_eval_1(state, player):
    """Dummy offensive eval from the spec: fewer opponent pieces = better (plus noise)."""
    board = state["board"]
    opp = _opponent(player)
    opp_left = _count_pieces(board, opp)
    return 2 * (32 - opp_left) + random.random()


def offensive_eval_2(state, player):
    """More aggressive eval: push advanced, create imminent threats, and capture."""
    board = state["board"]
    opp = _opponent(player)

    own_left = _count_pieces(board, player)
    opp_left = _count_pieces(board, opp)

    advancement = _advancement_score(board, player)
    almost_win = _almost_win(board, player)
    threatened = _pieces_under_attack(board, player)

    captures_so_far = state["captures"][player]

    # Linear combination (tuned to reliably beat Def1 in practice).
    value = (
        40 * (16 - opp_left)          # material advantage via captures
        + 6 * advancement             # keep moving forward
        + 80 * almost_win             # prioritize near-wins
        + 25 * captures_so_far        # prefer lines that actually captured
        - 12 * threatened             # avoid hanging pieces (but not too timid)
        + 3 * own_left                # slight preference for keeping pieces
    )
    return value + random.random()


def defensive_eval_2(state, player):
    """More defensive eval: keep material, protect pieces, and stop opponent advancement."""
    board = state["board"]
    opp = _opponent(player)

    own_left = _count_pieces(board, player)
    opp_left = _count_pieces(board, opp)

    own_threatened = _pieces_under_attack(board, player)
    opp_threatened = _pieces_under_attack(board, opp)

    opp_adv = _advancement_score(board, opp)
    opp_almost_win = _almost_win(board, opp)
    home = _home_row_pieces(board, player)
    connectivity = _connected_pairs(board, player)

    # Keep pieces, maintain a back line, reduce opponent progress.
    value = (
        50 * own_left
        - 10 * opp_left
        - 7 * opp_adv
        - 90 * opp_almost_win          # hard-stop "one step from losing"
        - 14 * own_threatened
        + 8 * opp_threatened
        + 6 * home
        + 3 * connectivity
    )
    return value + random.random()

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
