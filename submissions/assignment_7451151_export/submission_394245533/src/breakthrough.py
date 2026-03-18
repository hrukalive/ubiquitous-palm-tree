import random
from copy import deepcopy

from tqdm import tqdm

from games import Game


# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self):  # ⚠️ DO NOT CHANGE THIS FUNCTION
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",
            'captures': {"WHITE": 0, "BLACK": 0},
            'board': grid,
        }  # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):

        return state['to_move']


    def actions(self, state):

        player = state['to_move']
        board = state['board']
        moves = []
        direction = -1 if player == "WHITE" else 1
        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    nr = r + direction
                    if 0 <= nr < 8:
                        # Forward
                        if board[nr][c] == "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c)})
                        if c > 0 and board[nr][c - 1] == "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c - 1)})
                        elif c > 0 and board[nr][c - 1] != player and board[nr][c - 1] != "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c - 1)})
                        if c < 7 and board[nr][c + 1] == "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c + 1)})
                        elif c < 7 and board[nr][c + 1] != player and board[nr][c + 1] != "EMPTY":
                            moves.append({"from": (r, c), "to": (nr, c + 1)})
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

        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        board = deepcopy(state['board'])
        captures = deepcopy(state['captures'])
        fr, fc = action['from']
        tr, tc = action['to']
        if board[tr][tc] == opponent:
            captures[player] += 1
        board[tr][tc] = player
        board[fr][fc] = "EMPTY"
        return {
            'to_move': opponent,
            'captures': captures,
            'board': board
        }

    # Return the resulting state after applying the action to the current state.
    # The action is represented as a dict containing "to_move" (alternating),
    #      "captures" (updated captures) and "board" (updated grid).

    def utility(self, state, player):

        board = state['board']
        if player == "WHITE":
            if any(board[0][c] == "WHITE" for c in range(8)):
                return 99999
            if all(board[r][c] != "BLACK" for r in range(8) for c in range(8)):
                return 1
            if any(board[7][c] == "BLACK" for c in range(8)):
                return -1
        else:
            if any(board[7][c] == "BLACK" for c in range(8)):
                return 99999
            if all(board[r][c] != "WHITE" for r in range(8) for c in range(8)):
                return 1
            if any(board[0][c] == "WHITE" for c in range(8)):
                return -1
        return 0

    # Return the value to the perspective of the "player";
    #    Positive for win, negative for loss, 0 otherwise.

    def terminal_test(self, state):

        board = state['board']
        if any(board[0][c] == "WHITE" for c in range(8)):
            return True
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True
        white_left = any(board[r][c] == "WHITE" for r in range(8) for c in range(8))
        black_left = any(board[r][c] == "BLACK" for r in range(8) for c in range(8))
        if not white_left or not black_left:
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
        print(
            f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")


def count_pieces(state, player):
    return sum(row.count(player) for row in state['board'])


# Evaluation functions

def defensive_eval_1(state, player):
    return 2 * count_pieces(state, player) + random.random()


def offensive_eval_1(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    return 2 * (32 - count_pieces(state, opponent)) + random.random()


def defensive_eval_2(state, player):
    if state['to_move'] == player and any(
        state['board'][r][c] == player for r, c in [(0, i) if player == "WHITE" else (7, i) for i in range(8)]):
        return 9999  # Win condition

    score = 0
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    board = state['board']

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 10 #points for staying alive

                back_row = r + 1 if player == "WHITE" else r - 1
                if 0 <= back_row < 8:
                    for dc in [-1, 1]:
                        if 0 <= c + dc < 8 and board[back_row][c + dc] == player:
                            score += 2

                dist_to_goal = r if player == "WHITE" else (7 - r)
                score += dist_to_goal * 0.5

    return score + random.random()


def offensive_eval_2(state, player):
    board = state['board']
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    if any(board[0 if player == "WHITE" else 7][c] == player for c in range(8)):
        return 9999

    score = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == player:
                progress = (7 - r) if player == "WHITE" else r
                score += (progress ** 2)

                score += 5 #points for staying alive

            elif piece == opponent:
                opp_progress = r if player == "WHITE" else (7 - r)
                score -= (opp_progress ** 2)

    return score + random.random()

ag_eval_fn = defensive_eval_1  # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.


##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False):  # ⚠️ DO NOT CHANGE
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
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game,
                                                                                                                state)
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
        'final_state': game.display(state),
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
