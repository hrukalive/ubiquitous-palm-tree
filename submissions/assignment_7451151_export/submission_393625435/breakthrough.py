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
        return state["to_move"]

    def actions(self, state):
        ##########################################################################
        board = state["board"]
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        direction = -1 if player == "WHITE" else 1

        actions = []

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    nr = r + direction
                    if 0 <= nr < 8:
                        if board[nr][c] == "EMPTY":
                            actions.append({"from": (r, c), "to": (nr, c)})
                        if c - 1 >= 0 and board[nr][c - 1] == opponent:
                            actions.append({"from": (r, c), "to": (nr, c - 1)})
                        if c + 1 < 8 and board[nr][c + 1] == opponent:
                            actions.append({"from": (r, c), "to": (nr, c + 1)})

        return actions

    def result(self, state, action):
        ##########################################################################
        new_state = {
            "to_move": state["to_move"],
            "captures": state["captures"].copy(),
            "board": deepcopy(state["board"])
        }

        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        fr, fc = action["from"]
        tr, tc = action["to"]

        if new_state["board"][tr][tc] == opponent:
            new_state["captures"][player] += 1

        new_state["board"][tr][tc] = player
        new_state["board"][fr][fc] = "EMPTY"
        new_state["to_move"] = opponent

        return new_state

    def utility(self, state, player):
        ##########################################################################
        board = state["board"]

        white = 0
        black = 0

        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white += 1
                elif board[r][c] == "BLACK":
                    black += 1

        if any(board[0][c] == "WHITE" for c in range(8)) or black == 0:
            winner = "WHITE"
        elif any(board[7][c] == "BLACK" for c in range(8)) or white == 0:
            winner = "BLACK"
        elif len(self.actions(state)) == 0:
            winner = "BLACK" if state["to_move"] == "WHITE" else "WHITE"
        else:
            return 0

        return 1 if winner == player else -1

    def terminal_test(self, state):
        ##########################################################################
        board = state["board"]

        if any(board[0][c] == "WHITE" for c in range(8)):
            return True
        if any(board[7][c] == "BLACK" for c in range(8)):
            return True

        white_exists = False
        black_exists = False

        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_exists = True
                elif board[r][c] == "BLACK":
                    black_exists = True

        if not (white_exists and black_exists):
            return True

        if len(self.actions(state)) == 0:
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
    board = state["board"]
    own = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                own += 1
    return 2 * own + random.random()

def offensive_eval_1(state, player):
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                opp += 1
    return 2 * (32 - opp) + random.random()

def defensive_eval_2(state, player):
    board = state["board"]
    score = 0
    direction = -1 if player == "WHITE" else 1

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 2
                score += (7 - r) if player == "WHITE" else r
                nr = r + direction
                if 0 <= nr < 8:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and board[nr][nc] != "EMPTY" and board[nr][nc] != player:
                            score -= 1

    return score + random.random()

def offensive_eval_2(state, player):
    board = state["board"]
    score = 0
    direction = -1 if player == "WHITE" else 1
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 3
                score += (7 - r) if player == "WHITE" else r
                nr = r + direction
                if 0 <= nr < 8:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and board[nr][nc] == opponent:
                            score += 2

    return score + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.
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