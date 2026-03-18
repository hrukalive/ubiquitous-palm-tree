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
        player = state['to_move']
        board = state['board']
        legal_actions = []
        direction = -1 if player == "WHITE" else 1 # -1 moves up the grid if white, move down 1 if black

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    for dc in [-1, 0, 1]: # checks 3 directions: left-diagonal (-1), straight (0), and right-diagonal (1)
                        nr, nc = r + direction, c + dc
                        if 0 <= nr < 8 and 0 <= nc <8:
                            target = board[nr][nc]
                            if dc == 0 and target == "EMPTY": # rule: can only move straigt if it's an empty square
                                legal_actions.append({"from": (r, c), "to": (nr, nc)})
                            elif dc != 0 and target != player: # rule: diagonal move is allowed to empty spaces or oppenent spaces (capture)
                                legal_actions.append({"from": (r, c), "to": (nr, nc)})
        return legal_actions

    def result(self, state, action):
        new_state = deepcopy(state)
        r_f, c_f = action["from"]
        r_t, c_t = action["to"]
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        if new_state["board"][r_t][c_t] == opponent:
            new_state["captures"][player] += 1

        new_state["board"][r_f][c_f] = "EMPTY"
        new_state["board"][r_t][c_t] = player
        new_state["to_move"] = opponent
        return new_state

    def utility(self, state, player):
        if not self.terminal_test(state):
            return 0
        board = state['board']
        white_win = any(board[0][c] == "WHITE" for c in range(8)) or sum(row.count("BLACK") for row in board) == 0
        winner = "WHITE" if white_win else "BLACK"
        return 1 if winner == player else -1

    def terminal_test(self, state): # checks if game has reached a winning state
        board = state['board']
        for c in range(8): # condition 1: has any reached the other side
            if board[0][c] == "WHITE" or board[7][c] == "BLACK":
                return True
            white_pieces = sum(row.count("WHITE") for row in board) # condition 2: has player lost all their pieces
            black_pieces = sum(row.count("BLACK") for row in board)
            if white_pieces == 0 or black_pieces == 0:
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

# Evaluation Functions
def defensive_eval_1(state, player):
    return 2 * sum(row.count(player) for row in state['board']) + random.random()


def offensive_eval_1(state, player):
   opponent = "BLACK" if player == "WHITE" else "WHITE"
   opp_count = sum(row.count(opponent) for row in state['board']) 
   return 2 * (16 - opp_count) + random.random()


def defensive_eval_2(state, player):
    score = 0
    board = state['board']
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                dist_to_goal = r if player == "WHITE" else (7 - r)
                score += (8 - dist_to_goal) ** 2
    return score + random.random()


def offensive_eval_2(state, player):
    score = 0
    board = state['board']
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                progress = (7 - r) if player == "WHITE" else (7 - r) # calculates progress: distance from the starting edge
                score += (progress ** 2)

                if (player == "WHITE" and r == 1) or (player == "BLACK" and r == 6): # large bonus for being one move away from winning - heuristic
                    score += 100
    return score + random.random() # random noise will help break ties

ag_eval_fn = offensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_2  # ⚠️ Change this to your preferred evaluation function for comeptition.

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
