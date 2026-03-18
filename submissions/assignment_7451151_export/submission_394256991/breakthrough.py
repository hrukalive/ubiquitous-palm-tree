import random
from copy import deepcopy

from tqdm import tqdm

from games import Game
# Name : Aditya Manoj Krishna
# WPI ID : amkrishna@wpi.edu
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
        
        # White moves up (negative row index), Black moves down (positive row index)
        direction = -1 if player == "WHITE" else 1
        
        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    new_r = r + direction
                    # Ensure move is within vertical bounds
                    if 0 <= new_r < 8:
                        # Check three possible columns: straight, diagonal left, diagonal right
                        for new_c in [c - 1, c, c + 1]:
                            if 0 <= new_c < 8:
                                target = board[new_r][new_c]
                                if new_c == c: # Straight move
                                    if target == "EMPTY":
                                        legal_actions.append({"from": (r, c), "to": (new_r, new_c)})
                                else: # Diagonal move
                                    if target != player: # Can move to EMPTY or capture opponent
                                        legal_actions.append({"from": (r, c), "to": (new_r, new_c)})
        return legal_actions

    def result(self, state, action):
        new_state = deepcopy(state)
        f_r, f_c = action["from"]
        t_r, t_c = action["to"]
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        # Check for capture
        if new_state['board'][t_r][t_c] == opponent:
            new_state['captures'][player] += 1
        
        # Update board
        new_state['board'][t_r][t_c] = player
        new_state['board'][f_r][f_c] = "EMPTY"
        
        # Switch turn
        new_state['to_move'] = opponent
        return new_state

    def utility(self, state, player):
        # A win is 100, a loss is -100.
        # Check if current state is terminal and who won
        if self.terminal_test(state):
            # If it's WHITE's turn and terminal, BLACK must have just reached the end
            winner = "BLACK" if state['to_move'] == "WHITE" else "WHITE"
            return 100 if winner == player else -100
        return 0

    def terminal_test(self, state):
        board = state['board']
        # Condition 1: A piece reached the opposite side
        if any(cell == "WHITE" for cell in board[0]): return True
        if any(cell == "BLACK" for cell in board[7]): return True
        
        # Condition 2: A player has no pieces left (captured all)
        white_count = sum(row.count("WHITE") for row in board)
        black_count = sum(row.count("BLACK") for row in board)
        return white_count == 0 or black_count == 0

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
    # Basic defense: Focus on number of own pieces remaining
    own_pieces = sum(row.count(player) for row in state['board'])
    return own_pieces + random.random()

def offensive_eval_1(state, player):
    # Basic offense: Focus on how many opponent pieces are captured
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    opp_pieces = sum(row.count(opponent) for row in state['board'])
    return (16 - opp_pieces) + random.random()

def defensive_eval_2(state, player):
    # Advanced defense: Penalize opponent pieces getting closer to your home row
    score = 0
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    home_row = 7 if player == "WHITE" else 0
    
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == opponent:
                # Higher penalty if opponent is closer to row 7 (for white player) or 0 (for black player)
                dist_to_goal = abs(r - home_row)
                score -= (8 - dist_to_goal)
    return score + random.random()

def offensive_eval_2(state, player):
    # Advanced offense: Reward own pieces for getting closer to the enemy home row
    score = 0
    goal_row = 0 if player == "WHITE" else 7
    
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                dist_to_goal = abs(r - goal_row)
                score += (8 - dist_to_goal)
    return score + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Use a stronger eval for competition.

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