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
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
        return state["to_move"]

    def actions(self, state):
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        player=state["to_move"]
        board=state["board"]
        moves=[]
        if player == "WHITE":
            direction = -1
            opponent = "BLACK"
        else:
            direction = 1
            opponent = "WHITE"
        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    nr = r + direction
                    if 0 <= nr < 8:
                        if board[nr][c] == "EMPTY":
                            moves.append({"from": (r,c), "to": (nr, c)})
                        if c - 1 >= 0:
                            if board[nr][c - 1] in ["EMPTY", opponent]:
                                moves.append({"from": (r,c), "to": (nr, c - 1)})
                        nc = c+1
                        if 0 <= nc < 8 :
                            if board[nr][nc] in ["EMPTY", opponent]:
                                moves.append({"from": (r,c), "to": (nr, nc)})
        return moves

    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        new_state = deepcopy(state)
        board=new_state["board"]
        r1,c1=action["from"]
        r2,c2=action["to"]
        player = state["to_move"]
        if player == 'WHITE':
            opponent = "BLACK"
        else:
            opponent = "WHITE"
        if board[r2][c2] == opponent:
            new_state["captures"][player]+=1
        board[r2][c2] = player
        board[r1][c1]= "EMPTY"
        new_state["to_move"] = opponent
        return new_state


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if not self.terminal_test(state):
            return 0
        if state["to_move"] == "BLACK":
            winner ="WHITE"
        else:
            winner ="BLACK"
        if winner==player:
            return 1
        return -1

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]
        white_exists = False
        black_exists = False
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_exists=True
                    if r==0:
                        return True
                elif board[r][c] == "BLACK":
                    black_exists=True
                    if r==7:
                        return True
        return not white_exists or not black_exists

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

def defensive_eval_1(state, player):
    num_own = sum(row.count(player) for row in state["board"])
    return 2 * num_own + random.random()


def offensive_eval_1(state, player):
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    num_opponent = sum(row.count(opponent) for row in state["board"])
    return 2 * (32 - num_opponent) + random.random()

def defensive_eval_2(state, player):
    board = state["board"]
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 3
                if player == "WHITE" and r>=6:
                    score+=2
                if player == "BLACK" and r <=1:
                    score+=2
            elif board[r][c] == opponent:
                score -=3
    score -= 5 * state["captures"][opponent]
    return score + random.random()


def offensive_eval_2(state, player):
    board = state["board"]
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                if player == "WHITE":
                    score += (7-r)
                else:
                    score +=r
            elif board[r][c] == opponent:
                score -=2
    score += 5 * state["captures"][player]
    return score + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_2  # ⚠️ Change this to your preferred evaluation function for competition.

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
    print("Final Board")
    for row in state["board"]:
        print(row)
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
