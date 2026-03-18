
import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# ---------------------------------------------------------------------------
# Breakthrough game + heuristics
# This file is organized to match the report/video flow:
# 1) game model (state, legal actions, state transition, terminal/winner)
# 2) evaluation function designs (defensive vs offensive, two variants each)
# 3) match runner used by both demos and experiments
# ---------------------------------------------------------------------------

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
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
        return state["to_move"] # tell the engine whose turn it is 
    # search function need to know whose action to generate

    def actions(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return a list of dict containing a "from" tuple and a "to" tuple for each
        # legal move in this state.
        # For example, to move a piece from (6,0) to (5,0), the action is
        # represented as
        # {
        #     "from": (6,0),
        #     "to": (5,0)
        # }
        # And the function returns [{"from": (6,0), "to": (5,0)}, {"from": (6,0), "to": (5,1)}, ...]
        # Core move generator for tree search.
        # For each piece: try 1 forward step (empty only) and 2 forward diagonals
        # (capture only). This exactly encodes Breakthrough's legal move rules.
        board = state["board"]
        player = state["to_move"]
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        direction = -1 if player == "WHITE" else 1 # white moves upward (row - 1), black moves downward (row + 1)

        moves = []

        for r in range(8): 
            for c in range(8): 
                if board[r][c] != player: # find the player 
                    continue
                nr = r + direction 
                if not (0 <= nr < 8): 
                    continue
                
                if board[nr][c] == "EMPTY":  # forward move allowed only if target square is empty 
                    moves.append({"from": (r, c), "to": (nr, c)})

                # diagonal captures (only if the cell is occupied by opponent)
                if c - 1 >= 0 and board[nr][c - 1] == opponent: 
                    moves.append({"from": (r, c), "to": (nr, c - 1)})
                if c + 1 < 8 and board[nr][c + 1] == opponent: 
                    moves.append({"from": (r, c), "to": (nr, c + 1)})
        return moves
        # the branching function for game tree search 


    def result(self, state, action):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        # Pure transition function:
        # create a new state object instead of mutating the input state so search
        # can safely explore many hypothetical branches.
        new_state = { # apply one move and return the next state 
            "to_move": "BLACK" if state["to_move"] == "WHITE" else "WHITE",
            "captures": deepcopy(state["captures"]), # deep copy board and capture dict (sp original state is unchanged)
            "board": deepcopy(state["board"]),
        }

        fr, fc = action["from"] # move piece from source to destination 
        tr, tc = action["to"]
        mover = state["to_move"]
        target = new_state["board"][tr][tc]

        if target in ("WHITE", "BLACK") and target != mover: 
            new_state["captures"][mover] += 1 # if destination contains opponent piece, increment mover's capture counter 
        
        new_state["board"][tr][tc] = mover
        new_state["board"][fr][fc] = "EMPTY"
        return new_state # search explores hypothetical future states, so immutable-like behavior is important

    def winner(self, state): # helper function to decide if someone has won
        # Centralized win-condition checker used by utility/terminal_test.
        # Breakthrough ends when one side:
        # 1) reaches the opposite back rank, or
        # 2) captures all opponent pieces, or
        # 3) leaves opponent with no legal move.
        board = state["board"]

        # Breakthrough condition: reach opposite back rank 
        if any(board[0][c] == "WHITE" for c in range(8)): # white reaches row 0 
            return "WHITE"
        if any(board[7][c] == "BLACK" for c in range(8)): # black reaches row 7 
            return "BLACK"
        
        # All opponent pieces captured
        if state["captures"]["WHITE"] >= 16: # white captured all 16 black pieces 
            return "WHITE"
        if state["captures"]["BLACK"] >= 16: # black captured all 16 whtie pieces 
            return "BLACK"
        
        # No legal move => side to move loses
        if len(self.actions(state)) == 0:
            return "BLACK" if state["to_move"] == "WHITE" else "WHITE" # return white or black if game ended 
        
        return None # centralized winner logic prevents inconsistencies across terminal test and utility function

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        winner = self.winner(state) # convert terminal result into numeric reward for one player perspective 
        if winner is None: 
            return 0

        return 1 if winner == player else -1 # +1 if win and -1 if loss 

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.
        return self.winner(state) is not None # return true when winner(state) is not None

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
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def opponent(player): # helper function to flip player color 
    return "BLACK" if player == "WHITE" else "WHITE"

def piece_positions(state, player): # collect position of one player's pieces 
    board = state["board"]
    positions = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                positions.append((r, c)) # output list of (row, col) for that player 
    return positions # reused by multiple heuristic to avoid repeating board scans 

def progress_score(state, player): # measure how far pieces have advanced toward promotion row 
    # Larger is better for player (closer to promotion row)
    score = 0
    for r, c in piece_positions(state, player):
        score += (7 - r) if player == "WHITE" else r
    return score

def threat_count(state, player): # count immediate capture opportunities currently available 
    board = state["board"]
    opp = opponent(player)
    direction = -1 if player == "WHITE" else 1

    threats = 0 
    for r, c in piece_positions(state, player): # for each piece, checks forward diagonals for opponent pieces 
        nr = r + direction 
        if not (0 <= nr < 8):
            continue
        if c - 1 >= 0 and board[nr][c - 1] == opp:
            threats += 1
        if c + 1 < 8 and board[nr][c + 1] == opp:
            threats += 1
    return threats

def home_guard_count(state, player): # count pieces still on home row
    # defensive stability, protects against fast breakthrough 
    board = state["board"]
    home_row = 7 if player == "WHITE" else 0
    return sum(1 for c in range(8) if board[home_row][c] == player)

def defensive_eval_1(state, player): # conservative heuristic focused on survival and control 
    # encourages safe structure and minimizing risk 
    game = Breakthrough()
    if game.terminal_test(state): 
        return 10_000 * game.utility(state, player)  # Very large positive for win, very large negative for loss
    
    opp = opponent(player)
    my_piece = 16 - state["captures"][opp] # material difference (piece count)
    opp_piece = 16 - state["captures"][player]
    my_progress = progress_score(state, player)
    opp_progress = progress_score(state, opp) # opponent progress vs my progress (penalty for opponent advancement)
    my_guard = home_guard_count(state, player) # own home-row guards 
    opp_threats = threat_count(state, opp) # opponent immediate threads (penalty)

    # Design intent:
    # prioritize material + back-rank guards, and heavily punish opponent threats
    # and unchecked enemy progress.
    return (
        120 * (my_piece - opp_piece) + 12 * (my_guard) - 10 * (opp_threats) - 5 * (opp_progress - my_progress)
    )


def offensive_eval_1(state, player): # aggresive heuristic focused on attack 
    game = Breakthrough()
    if game.terminal_test(state): 
        return 10_000 * game.utility(state, player)
    
    opp = opponent(player)
    my_pieces = 16 - state["captures"][opp] # material difference 
    opp_pieces = 16 - state["captures"][player]
    my_progress = progress_score(state, player) # own progress 
    my_threats = threat_count(state, player) # own tactical threats 
    
    # Design intent:
    # push material edge + advancement + immediate tactical pressure.
    return (
        100 * (my_pieces - opp_pieces) + 15 * my_progress + 18 * my_threats + 35 * state["captures"][player] # captures already achieved
    )


def defensive_eval_2(state, player): # second defensive strategy, tuned to beat agressive play 
    # tuned to punish opponent attacking structure (good vs offensive_eval_1)
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    
    opp = opponent(player)
    my_pieces = 16 - state["captures"][opp]
    opp_pieces = 16 - state["captures"][player]
    my_guard = home_guard_count(state, player)
    opp_progress = progress_score(state, opp)
    opp_threats = threat_count(state, opp)
    my_threats = threat_count(state, player)
    
    # Compared to defensive_eval_1:
    # stronger penalties on enemy threats/progress, slightly more reward for
    # preserving defensive structure.
    return (
        130 * (my_pieces - opp_pieces) + 20 * my_guard - 14 * opp_progress - 24 * opp_threats + 6 * my_threats
    )


def offensive_eval_2(state, player):
    # tuned to break defensive setups (good vs defensive_eval_1)
    game = Breakthrough()
    if game.terminal_test(state):
        return 10_000 * game.utility(state, player)
    
    opp = opponent(player)
    my_pieces = 16 - state["captures"][opp]
    opp_pieces = 16 - state["captures"][player]
    my_progress = progress_score(state, player)
    opp_guard = home_guard_count(state, opp)
    my_threats = threat_count(state, player)

    # bonus for advanced pawns on 2nd/3rd rank from promotion side
    advanced_bonus = 0
    for r, c in piece_positions(state, player):
        if player == "WHITE" and r <= 2: 
            advanced_bonus += 1
        if player == "BLACK" and r >= 5: 
            advanced_bonus += 1
    
    # Compared to offensive_eval_1:
    # rewards deep advanced pawns and pressure, while directly penalizing an
    # opponent that still has a strong home-row shield.
    return (
        105 * (my_pieces - opp_pieces) 
        + 19 * my_progress
        + 24 * my_threats
        + 28 * advanced_bonus 
        - 10 * opp_guard
    )

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run one full game and collect metrics used in the report:
    winner, move count, captures, average time per move, and nodes expanded.

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

