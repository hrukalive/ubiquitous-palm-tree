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
        return state["to_move"]

    def actions(self, state):
        player = state["to_move"]
        board = state["board"]
        moves = []

        # WHITE moves upward (decreasing row), BLACK moves downward (increasing row)
        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                newR = r + direction

                if not (0 <= newR < 8):
                    continue
                if board[newR][c] == "EMPTY":
                    moves.append({"from": (r,c), "to": (newR,c)})

                for diaganolCol in [-1,1]:
                    newC = c + diaganolCol
                    if 0 <= newC < 8 and board[newR][newC] == opponent:
                        moves.append({"from": (r,c), "to": (newR,newC)})

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
        board = deepcopy(state["board"])
        captures = {"WHITE": state["captures"]["WHITE"], "BLACK": state["captures"]["BLACK"]}
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        fromRow, fromCol = action["from"]
        toRow, toCol = action["to"]

        if board[toRow][toCol] == opponent:
            captures[player] += 1

        board[toRow][toCol] = player
        board[fromRow][fromCol] = "EMPTY"

        nextPlayer = "WHITE" if player == "BLACK" else "BLACK"

        return {
            'to_move': nextPlayer,
            'captures': captures,
            'board': board,
        }


        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).


    def utility(self, state, player):
        # Called only on terminal states.
        # The player who just moved (opponent of to_move) has won.
        winner = "BLACK" if state["to_move"] == "WHITE" else "WHITE"
        if winner == player:
            return 1
        else:
            return -1

        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.


    def terminal_test(self, state):
        board = state["board"]

        for c in range(8):
            if board[0][c] == "WHITE":
                return True

        for c in range(8):
            if board[7][c] == "BLACK":
                return True

        whiteCount = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        blackCount = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")

        if whiteCount == 0 or blackCount == 0:
            return True

        if not self.actions(state):
            return True

        return False

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




# Evaluation functions

def _count_pieces(board, player):
    """Count remaining pieces for a player."""
    return sum(1 for r in range(8) for c in range(8) if board[r][c] == player)


def defensive_eval_1(state, player):
    board = state["board"]
    ownPieces = _count_pieces(board, player)
    return 2 * ownPieces + random.random()


def offensive_eval_1(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opponentPieces = _count_pieces(board, opponent)
    return 2 * opponentPieces + random.random()


def defensive_eval_2(state, player):
    """
    Key ideas:
    - Value own pieces remaining (like defensive_eval_1) but also penalize
      opponent pieces that are far advanced (close to our home row).
    - Reward pieces that are well-protected (horizontally connected).
    - Penalize pieces that are under attack (diagonal attack from opponent).
    - Reward pieces in the home row area for blocking.

    For WHITE: home rows are 6-7 (bottom), advancing means going toward row 0.
    For BLACK: home rows are 0-1 (top), advancing means going toward row 7.
    """
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    score = 0.0


    if player == "WHITE":
        home_rows = [6, 7]
        opponent_advance_dir = 1  # BLACK advances downward (increasing row)
        own_advance_row = lambda r: 7 - r  # how far WHITE has advanced
    else:
        home_rows = [0, 1]
        opponent_advance_dir = -1  # WHITE advances upward (decreasing row)
        own_advance_row = lambda r: r  # how far BLACK has advanced

    own_piece_count = 0
    opp_piece_count = 0

    for r in range(8):
        for c in range(8):
            cell = board[r][c]

            if cell == player:
                own_piece_count += 1;
                if c > 0 and board[r][c - 1] == player:
                    score += 0.5
                if c < 7 and board[r][c + 1] == player:
                    score += 0.5

                if r in home_rows:
                    score += 1.0

                if player == "WHITE":
                    for diagonalCol in [-1,1]:
                        attackRow, attackCol = r - 1, c + diagonalCol
                        if 0 <= attackRow < 8 and 0 <= attackCol < 8 and board[attackRow][attackCol] == opponent:
                            score -= 1.5
                else:
                    # WHITE attacks from below (row r+1) diagonally
                    for diagonalCol in [-1, 1]:
                        attackRow, attackCol = r + 1, c + diagonalCol
                        if 0 <= attackRow < 8 and 0 <= attackCol < 8 and board[attackRow][attackCol] == opponent:
                            score -= 1.5
            elif cell == opponent:
                opp_piece_count += 1;

                # Penalize heavily for opponent pieces that are deep in our territory
                if player == "WHITE":
                    # Opponent (BLACK) advances toward row 7; penalize by how close they are
                    danger = r  # higher row = more danger for WHITE
                    score -= 1.5 * danger / 7.0
                else:
                    # Opponent (WHITE) advances toward row 0; penalize by how close they are
                    danger = 7 - r  # lower row = more danger for BLACK
                    score -= 1.5 * danger / 7.0

    score += 2.5 * own_piece_count

    # Tiebraker for equally good moves
    return score + random.random()


def offensive_eval_2(state, player):
    """
    Offensive Evaluation 2:
    Aggressive heuristic designed to win by pushing pieces forward fast
    while blocking opponent near-wins.

    Key ideas:
    - Reward advancement: pieces closer to the enemy home row score higher.
    - Large bonus for pieces on the penultimate row (one step from winning),
      scaled by whether they are safe or under attack.
    - Emergency penalty: if the opponent has a piece on their penultimate row
      (one step from winning), apply a heavy negative score to force blocking.
    - Bonus for threatening diagonal captures to maintain board pressure.
    - Penalize opponent pieces remaining and reward own captures.
    - Small survival bonus for own piece count so reckless trading is avoided.

    For WHITE: home = rows 6-7, target = row 0, penultimate = row 1.
    For BLACK: home = rows 0-1, target = row 7, penultimate = row 6.
    """
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    score = 0.0
    own_piece_count = 0
    opp_piece_count = 0

    # Penultimate rows (one step from winning)
    own_penultimate = 1 if player == "WHITE" else 6
    opp_penultimate = 6 if player == "WHITE" else 1

    for r in range(8):
        for c in range(8):
            cell = board[r][c]

            if cell == player:
                own_piece_count += 1

                # Reward advancement distance from home
                advance = (7 - r) if player == "WHITE" else r
                score += 2.0 * advance

                # Bonus for pieces on penultimate row (one move from winning)
                if r == own_penultimate:
                    safe = True
                    attack_dir = -1 if player == "WHITE" else 1
                    for dc in [-1, 1]:
                        ar, ac = r + attack_dir, c + dc
                        if 0 <= ar < 8 and 0 <= ac < 8 and board[ar][ac] == opponent:
                            safe = False
                    score += 15.0 if safe else 8.0

                # Bonus for threatening a diagonal capture next move
                attack_row = r - 1 if player == "WHITE" else r + 1
                if 0 <= attack_row < 8:
                    for dc in [-1, 1]:
                        ac = c + dc
                        if 0 <= ac < 8 and board[attack_row][ac] == opponent:
                            score += 1.0

            elif cell == opponent:
                opp_piece_count += 1

                # Emergency penalty: opponent is one step from winning
                if r == opp_penultimate:
                    safe = True
                    block_dir = 1 if player == "WHITE" else -1
                    for dc in [-1, 1]:
                        ar, ac = r + block_dir, c + dc
                        if 0 <= ar < 8 and 0 <= ac < 8 and board[ar][ac] == player:
                            safe = False  # we can capture it
                    # If we cannot capture it next move it is an emergency
                    score -= 20.0 if safe else 5.0

    # Penalize opponent pieces remaining
    score += 2.5 * (16 - opp_piece_count)

    # Reward own captures (aggressive tempo)
    score += 1.5 * state["captures"][player]

    # Small survival bonus so we do not trade pieces recklessly
    score += 0.5 * own_piece_count

    # Tiebreaker for equally good moves
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
