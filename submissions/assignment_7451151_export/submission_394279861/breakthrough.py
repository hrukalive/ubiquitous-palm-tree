import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

import random

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
        #already defined in dictionary in init, changing states handled in results
        return state['to_move']

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
        actions = []
        board = state['board']
        player = state['to_move']

        # black moves down the board (+), white moves up (neg) 
        if player == "WHITE":
            opponent = "BLACK"
            direction = -1
        else:
            opponent = "WHITE"
            direction = 1

        for r in range(8):
            for c in range(8):
                if board[r][c] != player:
                    continue

                #forward
                next_row_pos = r + direction
                if next_row_pos >= 0 and next_row_pos < 8:
                    if board[next_row_pos][c] == 'EMPTY':
                        actions.append({
                            "from": (r, c),
                            "to": (next_row_pos, c)
                        })

                    #diagonal left
                    if (c - 1) >= 0:
                        if board[next_row_pos][c - 1] in ["EMPTY", opponent]:
                            actions.append({
                                "from": (r, c),
                                "to": (next_row_pos, (c - 1))
                            })

                    #diagonal right
                    if (c + 1) < 8:
                        if board[next_row_pos][c + 1] in ["EMPTY", opponent]:
                            actions.append({
                                "from": (r, c),
                                "to": (next_row_pos, c + 1)
                            })

        return actions

    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        new_state = deepcopy(state)

        board = new_state['board']
        player = state['to_move']
        if player == "WHITE":
            opponent = "BLACK"
        else:
            opponent = "WHITE"

        from_r, from_c = action["from"]
        to_r, to_c = action["to"]

        board[from_r][from_c] = "EMPTY"

        if board[to_r][to_c] == opponent:
            new_state['captures'][player] += 1

        board[to_r][to_c] = player

        # changes player
        new_state['to_move'] = opponent

        return new_state


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        board = state['board']
        white_win = False 
        black_win = False

        for c in range(8):
            if board[0][c] == "WHITE":
                white_win = True
        
        for c in range(8):
            if board[7][c] == "BLACK":
                black_win = True

        white_count = 0
        black_count = 0

        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_count += 1
                elif board[r][c] == "BLACK":
                    black_count += 1

        if white_win or black_count == 0:
            winner = "WHITE"
        elif black_win or white_count == 0:
            winner = "BLACK"
        else:
            return 0

        if winner == player:
            return 1
        else: 
            return -1


    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        board = state['board']

        for c in range(8):
            if board[0][c] == "WHITE":
                return True
            
        for c in range(8):
            if board[7][c] == "BLACK":
                return True
        

        #Check if all pieces have been captured
        white_count = 0
        black_count = 0

        for r in range(8):
            for c in range(8):
                if board[r][c] == "WHITE":
                    white_count += 1
                elif board[r][c] == "BLACK":
                    black_count += 1

        if white_count == 0 or black_count == 0:
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


# Evaluation functions

def defensive_eval_1(state, player):
    # Dummy function provided
    board = state['board']

    num_own_pieces = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                num_own_pieces += 1
    
    return 2 * num_own_pieces + random.random()


def offensive_eval_1(state, player):
    # Dummy function provided
    board = state['board']

    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"

    num_opponent_pieces = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                num_opponent_pieces += 1
    
    
    return 2 * (32 - num_opponent_pieces) + random.random()


def defensive_eval_2(state, player):
    # Attempting to maintain a tight formation
    board = state['board']
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"

    diff_my_pieces = 0
    diff_opp_pieces = 0
    opponent_advances = 0
    horizontal_connections = 0
    vertical_connections = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                diff_my_pieces += 1

                if c + 1 < 8 and board[r][c + 1] == player:
                    horizontal_connections += 1

                if r + 1 < 8 and board[r + 1][c] == player:
                    vertical_connections += 1

            elif board[r][c] == opponent:
                diff_opp_pieces += 1

                if opponent == "WHITE":
                    opponent_advances += (7 - r)
                else:
                    opponent_advances += r
                    
    return (8 * (diff_my_pieces - diff_opp_pieces) - 6 * opponent_advances + 3 * horizontal_connections + 2 * vertical_connections)


def offensive_eval_2(state, player):
    board = state['board']
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    
    diff_my_pieces = 0
    diff_opp_pieces = 0
    my_advances = 0
    opponent_advances = 0
    almost_win = 0
    opp_under_attack = 0

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                diff_my_pieces += 1

                #White wants to reach row 0; Black to row 7
                if player == "WHITE":
                    my_advances += (7 - r)
                    if r == 1:
                        almost_win += 1
                else:
                    my_advances += r
                    if r == 6:
                        almost_win += 1
            elif board[r][c] == opponent:
                diff_opp_pieces += 1

                if opponent == "WHITE":
                    opponent_advances += (7 - r)
                else:
                    opponent_advances += r

    # Countinf opponent pieces that are under attack 
    if player == "WHITE":
        direction = -1
    else:
        direction = 1

    for r in range(8):
        for c in range(8):
            if board[r][c] == opponent:
                #checks if capture is possible
                for x in [-1, 1]:
                    new_r = r - direction
                    new_c = c + x
                    if (new_r >= 0 and new_r < 8) and (new_c >= 0 and new_c < 8):
                        if board[new_r][new_c] == player:
                            opp_under_attack += 1


    
    return (10 * (diff_my_pieces - diff_opp_pieces) + 4 * (my_advances - opponent_advances) + 25 * almost_win + 3 * opp_under_attack)

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
