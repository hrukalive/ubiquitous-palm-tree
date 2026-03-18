import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# Helper functions

def _opponent(player: str) -> str:
    return "BLACK" if player == "WHITE" else "WHITE"

def _in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8

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
        player = state["to_move"]
        opp = _opponent(player)
        board = state["board"]

        dr = -1 if player == "WHITE" else 1

        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                # forward move: must land on an empty square
                nr, nc = r + dr, c
                if _in_bounds(nr, nc) and board[nr][nc] == "EMPTY":
                    moves.append({"from": (r, c), "to": (nr, nc)})
                
                # diagonal left move: Can be empty or can capture opponent
                nr, nc = r + dr, c - 1
                if _in_bounds(nr, nc) and board[nr][nc] in ("EMPTY", opp):
                    moves.append({"from": (r, c), "to": (nr, nc)})
                
                # diagonal right move: can be empty or can capture opponent
                nr, nc = r + dr, c + 1
                if _in_bounds(nr, nc) and board[nr][nc] in ("EMPTY", opp):
                    moves.append({"from": (r, c), "to": (nr, nc)})
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
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        # "captures" (updated captures) and "board" (updated grid).
        player = state["to_move"]
        opp = _opponent(player)

        (fr, fc) = action["from"]
        (tr, tc) = action["to"]

        new_board = [row[:] for row in state["board"]]
        new_captures = dict(state["captures"])

        assert new_board[fr][fc] == player, "Invalid Action"

        if new_board[tr][tc] == opp:
            new_captures[player] += 1
        
        new_board[fr][fc] = "EMPTY"
        new_board[tr][tc] = player

        return {"to_move": opp, "captures": new_captures, "board": new_board,}
    


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if not self.terminal_test(state):
            return 0
        
        board = state["board"]

        white_reached = any(board[0][c] == "WHITE" for c in range(8))
        black_reached = any(board[7][c] == "BLACK" for c in range(8))

        white_left = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        black_left = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")

        winner = None
        if white_reached or black_left == 0:
            winner = "WHITE"
        elif black_reached or white_left == 0:
            winner = "BLACK"

        if winner is None:
            return 0
        return 1 if winner == player else -1


    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state["board"]

        # There are two terminal states in this game
        # the first being if a player has reached the furthest row
        # the second being if all of an opponents pieces were eliminates

        # Reached the far row:
        if any(board[0][c] == "WHITE" for c in range (8)):
            return True
        if any(board[7][c] == "BLACK" for c in range (8)):
            return True
        
        # Opponent Eliminated:
        white_left = sum(1 for r in range(8) for c in range(8) if board[r][c] == "WHITE")
        black_left = sum(1 for r in range(8) for c in range(8) if board[r][c] == "BLACK")

        return white_left == 0 or black_left == 0


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
        return None



def _count_pieces(board, color:str) -> int:
    return sum(1 for r in range(8) for c in range(8) if board[r][c] == color)

# Evaluation functions

def defensive_eval_1(state, player):
    # 2 * (# own pieces remaining) + noise
    own_remaining = _count_pieces(state["board"], player)
    return 2 * own_remaining + random.random()
    

def offensive_eval_1(state, player):
    # 2 * (32 - # opponent pieces remaining) + noise
    opp_remaining = _count_pieces(state["board"], _opponent(player))
    return 2 * (32 - opp_remaining) + random.random()


def _dir(player):
    return -1 if player == "WHITE" else 1

def _count(board, color):
    return sum(1 for r in range(8) for c in range(8) if board[r][c] == color)

def _almost_win(board, player):
    row = 1 if player == "WHITE" else 6
    return sum(1 for c in range(8) if board [row][c] == player)

def _progress(board, player):
    state = 0
    if player == "WHITE":
        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    state += (7 - r)
    else:
        for r in range(8):
            for c in range(8):
                if board[r][c] == "BLACK":
                    state += r
    return state

def _under_attack(board, player):
    opp = _opponent(player)
    dr_opp = _dir(opp)
    threatened = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue
            sr = r - dr_opp  
            if _in_bounds(sr, c-1) and board[sr][c-1] == opp:
                threatened += 1
                continue
            if _in_bounds(sr, c+1) and board[sr][c+1] == opp:
                threatened += 1
                continue
    return threatened

def _threatening_captures(board, player):
    opp = _opponent(player)
    dr = _dir(player)
    threats = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] != player:
                continue
            nr = r + dr
            for nc in (c-1, c+1):
                if _in_bounds(nr, nc) and board[nr][nc] == opp:
                    threats += 1
    return threats

def defensive_eval_2(state, player):
    board = state["board"]
    opp = _opponent(player)

    my_pieces = _count(board, player)
    my_threatened = _under_attack(board, player)

    opp_almost = _almost_win(board, opp)
    opp_prog = _progress(board, opp)

    score = 0.0
    score += 12.0 * my_pieces
    score -= 18.0 * my_threatened       
    score -= 250.0 * opp_almost         
    score -= 3.0 * opp_prog            
    return score + 0.01 * random.random()

def offensive_eval_2(state, player):
    board = state["board"]
    opp = _opponent(player)

    my_almost = _almost_win(board, player)
    opp_almost = _almost_win(board, opp)
    my_prog = _progress(board, player)
    my_threats = _threatening_captures(board, player)

    my_threatened = _under_attack(board, player)

    my_pieces = _count(board, player)
    opp_pieces = _count(board, opp)

    score = 0.0
    score += 200.0 * my_almost         
    score -= 220.0 * opp_almost         
    score += 4.0 * my_prog            
    score += 12.0 * my_threats     
    score += 8.0 * my_pieces
    score -= 10.0 * opp_pieces

    score -= 35.0 * my_threatened      

    return score + 0.01 * random.random()
    

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