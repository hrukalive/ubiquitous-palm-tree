import random
from copy import deepcopy

from tqdm import tqdm
import numpy as np
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
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".

    def actions(self, state):
        player = self.to_move(state)
        board = state["board"]
        actions = []
        if player == "WHITE":
            direction = -1
        else:
            direction = 1

        for row in range(8):
            for col in range(8):
                #if it's not a piece skip
                if board[row][col] != player:
                    continue
                
                #if its at the end of the board skip
                next_row = row + direction
                if not (0 <= next_row < 8):
                    continue
                
                #move forward
                if board[next_row][col] == "EMPTY":
                    actions.append({"from": (row, col), "to": (next_row, col)})

                #move diagnol
                for dc in (-1, 1):
                    next_col = col + dc
                    #out of bounds
                    if not (0 <= next_col < 8):
                        continue
                    if board[next_row][next_col] != player:
                        actions.append({"from": (row, col), "to": (next_row, next_col)})

        return actions
                    
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

    def result(self, state, action):
        if action is None:
            print("action is none")
            return state

        board = deepcopy(state["board"])
        player = state["to_move"]
        ogCoord = action["from"]
        newCoord = action["to"]
        capture = state['captures'].copy()

        if board[newCoord[0]][newCoord[1]] != "EMPTY":
            capture[player] +=1


        board[ogCoord[0]][ogCoord[1]] = "EMPTY"
        board[newCoord[0]][newCoord[1]] = player


        player = "BLACK" if player == "WHITE" else "WHITE"

        return {
            'to_move': player, 
            'captures': capture, 
            'board': board,
        }

        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).


    def utility(self, state, player):
        board = state["board"]
        capture = state["captures"]

        winner = None

        for square in board[0]:
            if square == "WHITE":
                winner = "WHITE"
        
        for square in board[7]:
            if square == "BLACK":
                winner = "BLACK"
        
        if capture["WHITE"] == 16:
            winner = "WHITE"
        if capture["BLACK"] == 16:
            winner = "BLACK"

        if winner == player:
            return np.inf

        if winner:
            return -np.inf
        
        return 0
        
        
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.


    def terminal_test(self, state):
        return self.utility(state, state["to_move"]) != 0 or len(self.actions(state)) == 0
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
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



##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_pieces_remaining = 16 - state["captures"][opponent]
    return 2 * own_pieces_remaining + random.random()


def offensive_eval_1(state, player):
    opponent_pieces_remaining = 16 - state["captures"][player]
    return 2 * (32 - opponent_pieces_remaining) + random.random()


def defensive_eval_2(state, player):
    #This one I want to be a protection score aka if each pawn on the board is protected by another one
    board = state["board"]
    ownDir = -1 if player == "WHITE" else 1

    pawns = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == player:
                pawns.append((row, col))

    protectedCount = 0

    for row, col in pawns:
        supportRow = row - ownDir
        if not (0 <= supportRow < 8):
            continue

        leftSupportCol = col - 1
        rightSupportCol = col + 1

        hasLeftSupport = 0 <= leftSupportCol < 8 and board[supportRow][leftSupportCol] == player
        hasRightSupport = 0 <= rightSupportCol < 8 and board[supportRow][rightSupportCol] == player

        if hasLeftSupport or hasRightSupport:
            protectedCount += 1
    
    #reuse logic form eval 1
    allyComp = defensive_eval_1(state, player)
    
    return (2.5*protectedCount) + allyComp


def offensive_eval_2(state, player):
    # the main objective of this offensive one is to really push for the backrank win
    #firstly have a score of how far you are from the back rank (highly weighted)
    board = state["board"]
    opponent = "BLACK" if player == "WHITE" else "WHITE"

    pawns = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == player:
                pawns.append((row, col))


    backRank = 0 if player == "WHITE" else 7

    distances = []
    for pawn in pawns:
        row = pawn[0]
        distanceToBackrank = abs(row - backRank)
        distances.append(distanceToBackrank)

    closestProgress = 7 - min(distances)
    closestProgress = closestProgress * closestProgress

    # Penalty for threatened pawns; reduced if its protected
    threatenedPenalty = 0
    oppDir = 1 if opponent == "BLACK" else -1
    ownDir = -1 if player == "WHITE" else 1

    for row, col in pawns:
        threateningEnemyPositions = []

        enemyRow = row - oppDir
        if 0 <= enemyRow < 8:
            for dc in (-1, 1):
                enemyCol = col - dc
                if 0 <= enemyCol < 8 and board[enemyRow][enemyCol] == opponent:
                    threateningEnemyPositions.append((enemyRow, enemyCol))

        if threateningEnemyPositions:
            canTakeBack = False

            # If enemy captures onto, can another friendly pawn recapture
            supportRow = row - ownDir
            if 0 <= supportRow < 8:
                leftSupportCol = col - 1
                rightSupportCol = col + 1

                if 0 <= leftSupportCol < 8 and board[supportRow][leftSupportCol] == player:
                    canTakeBack = True
                elif 0 <= rightSupportCol < 8 and board[supportRow][rightSupportCol] == player:
                    canTakeBack = True

            threatenedPenalty += 0.5 if canTakeBack else 1.0

    # Capture pressure from offensive_eval_1, but lower priority than breakthrough pressure.
    captureComponent = offensive_eval_1(state, player)

    return (10 * closestProgress) - (12 * threatenedPenalty) + (2 * captureComponent)

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
