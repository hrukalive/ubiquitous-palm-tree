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
        return state['to_move']


    def actions(self, state):
        """Return the list of legal moves for the current player"""

        player = state['to_move']
        board = state['board']
        moves = []

        # White moves upward, Black moves downward
        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue
                nr = r + direction
                if not (0 <= nr < 8):
                    continue
                # Forward move where no capture is allowed of the opponent is there
                if board[nr][c] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, c)})
                # Diagonal captures/moves
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc <8:
                        # Can move diagonally foward if empty
                        # If occupied by an opponent, capture
                        if board[nr][nc] != player:
                            moves.append({"from": (r, c), "to": (nr, nc)})
        return moves

    def result(self, state, action):
        """Return new state after an action"""
        board = deepcopy(state['board'])
        captures = dict(state['captures'])
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        fr, fc = action['from']
        tr, tc = action['to']

        # Check capture
        if board[tr][tc] == opponent:
            captures[player] += 1

        board[tr][tc] = player
        board[fr][fc] = "EMPTY"

        next_player = "BLACK" if player == "WHITE" else "WHITE"
        return {
            'to_move': next_player,
            "captures": captures,
            'board': board,
        }


    def utility(self, state, player):
        """Return utility value from the perspective of the player"""
        board = state['board']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Checks for the win conditions
        # Player reached opponent's home row
        home_row_player = 0 if player == "WHITE" else 7
        home_row_opponent = 7 if player == "WHITE" else 0

        if any(board[home_row_player][c] == player for c in range(8)):
            return 1 # player wins
        if any(board[home_row_opponent][c] == opponent for c in range(8)):
            return -1

        # Count pieces
        player_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)
        opponent_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent)

        if player_pieces == 0:
            return -1
        if opponent_pieces == 0:
            return 1

        # No moves for current player means loss for that player
        if not self.actions(state):
            if state['to_move'] == player:
                return -1
            else:
                return 1
        return 0

    def terminal_test(self, state):
        """Return True if the game is over, False otherwise"""
        board = state['board']
        # White wins by reaching row 0
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True
        # BLACK wins by reaching row 7
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True
        # Check if either player has no pieces left
        white_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        black_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")
        if white_pieces == 0 or black_pieces == 0:
            return True
        # Check if current player has no moves
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

def defensive_eval_1(state, player):
    """More pieces remaing = higher value"""
    board = state['board']
    own_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == player)
    return 2 * own_pieces + random.random()


def offensive_eval_1(state, player):
    """Fewer opponent pieces = higher value."""
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state['board']
    opp_pieces = sum(1 for r in range(8) for c in range(8) if board[r][c] == opponent)
    return 2 * (32 - opp_pieces) + random.random()


def defensive_eval_2(state, player):
    """
    - Reward having more pieces
    - Reward pieces that are further back (harder to capture)
    - Penalize opponent pieces that have advanced far into our territory
    - Small random noise for tie-breaking.
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    own_pieces = 0
    own_advancement = 0 # own pieces' advancement toward goal
    opp_advancement = 0  # how far opponent pieces have advanced to player side

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own_pieces += 1
                # For white, advancement = 7-r (closer to row 0 = more advanced)
                # For black, advancement = r (close to row 7 = more advanced)
                if player == "WHITE":
                    own_advancement += (7 - r)
                else:
                    own_advancement += r
            elif board[r][c] == opponent:
                # Opponent advancement into player territory
                if player == "WHITE":
                    # Opponent (Black) advancing means increasing r
                    opp_advancement += r
                else:
                    # Opponent (White) advancing means decreasing r
                    opp_advancement += (7 - r)

    # Defensive: value own pieces highly, penalize opponent advancement
    score = (3 * own_pieces) - (0.5 * opp_advancement) + random.random()
    return score


def offensive_eval_2(state, player):
    """
    - Reward captures (opponent pieces lost)
    - Reward pieces that have advanced further toward the goal
    - Penalize opponent piece count
    - Small random noise for tie-breaking.
    """
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    own_pieces = 0
    own_advancement = 0
    opp_pieces = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                # Reward advancement toward the opponent's home row
                if player == "WHITE":
                    own_advancement += (7 - r) # row 0 is goal, so 7-r measures the distance traveled
                else:
                    own_advancement += r # row 7 is goal
            elif board[r][c] == opponent:
                opp_pieces += 1

    captures = state['captures'][player]
    score = (2 * own_advancement) + (3 * captures) + (2 * (16 - opp_pieces)) + random.random()
    return score

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
