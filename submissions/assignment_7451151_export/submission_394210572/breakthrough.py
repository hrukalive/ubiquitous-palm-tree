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
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the player to move in this state. Possible values: "WHITE" or "BLACK".
        
        # Pull the next player from the dictionary
        return state['to_move']

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

        # start by pulling the board
        boardy = state['board']

        # check whose move it is! 
        player = state['to_move']
        
        # we will define now if the player is moving up or down the board
        # we also get who the other player is in this part...
        movey = 0
        if (player == 'WHITE'):
            movey = -1
            badGuy = "BLACK"
        elif (player == 'BLACK'):
            movey = 1
            badGuy = "WHITE"

        # make a list for the moves'
        moves = []

        # loop through the grid
        for checkyY in range(0, 8):
            for checkyX in range(0, 8):
                # we are only going to check pieces for the current player
                if (player == boardy[checkyY][checkyX]):

                    # look at the possible left move (relative to the board frame)
                    lefty = (checkyX - 1, checkyY + movey)
                    # for the move to pass, it needs to meet three criteria
                    #  - the move must be within the x bounds of the board
                    #  - the move must be within the y bounds of the board
                    #  - the space must be either empty of contain an opponent piece
                    if ((0 <= lefty[0] < 8) and 
                        (0 <= lefty[1] < 8) and 
                        ((boardy[lefty[1]][lefty[0]] == 'EMPTY') or (boardy[lefty[1]][lefty[0]] == badGuy))):
                        # add the move to moves if it passes!
                        moves.append({
                            "from": (checkyY, checkyX),
                            "to": (lefty[1], lefty[0])
                        })

                    # look at the possible forward move
                    fronty = (checkyX, checkyY + movey)
                    # for the move to pass, it needs to meet two criteria
                    #  - the move must be within the y bounds of the board
                    #  - the space must be empty for forward moves
                    if ((0 <= fronty[1] < 8) and 
                        (boardy[fronty[1]][fronty[0]] == 'EMPTY')):
                        # add the move to moves if it passes!
                        moves.append({
                            "from": (checkyY, checkyX),
                            "to": (fronty[1], fronty[0])
                        })

                    # look at the possible right move (relative to the board frame)
                    righty = (checkyX + 1, checkyY + movey)
                    # for the move to pass, it needs to meet three criteria
                    #  - the move must be within the x bounds of the board
                    #  - the move must be within the y bounds of the board
                    #  - the space must be either empty of contain an opponent piece
                    if ((0 <= righty[0] < 8) and 
                        (0 <= righty[1] < 8) and 
                        ((boardy[righty[1]][righty[0]] == 'EMPTY') or (boardy[righty[1]][righty[0]] == badGuy))):
                        # add the move to moves if it passes!
                        moves.append({
                            "from": (checkyY, checkyX),
                            "to": (righty[1], righty[0])
                        })

        # we will end by returning the list of possible moves! Yay!    
        return moves 

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
        
        # start by pulling the board
        boardy = [row[:] for row in state['board']]

        # check whose move it is! 
        player = state['to_move']
        # we will also get who the other player is
        if (player == 'WHITE'):
            badGuy = "BLACK"
        elif (player == 'BLACK'):
            badGuy = "WHITE"


        # get the captures!
        captures = dict(state['captures'])
        
        # fix the coordinate systems
        fromyRow, fromyCol = action['from']
        toieRow, toieCol = action['to']

        fx, fy = fromyCol, fromyRow
        tx, ty = toieCol, toieRow

        # increment captures if a piece is taken
        if (boardy[ty][tx] == badGuy):
            captures[player] = captures[player] + 1

        # set the old place as empty
        boardy[fy][fx] = 'EMPTY'

        # update the spot to the correct player
        boardy[ty][tx] = player

        if (player == 'WHITE'):
            nextPlayer = 'BLACK'
        elif (player == 'BLACK'):
            nextPlayer = 'WHITE'

        return {
            'to_move': nextPlayer,
            'captures': captures,
            'board': boardy
        }





    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

        # start by pulling the board
        boardy = state['board']

        # check to see if the any pieces hace reached the other side
        for spoty in range(0, 8):
            # check the white pieces
            if (boardy[0][spoty] == 'WHITE'):
                if (player == 'WHITE'):
                    return 1
                else:
                    return -1
            
            # check the black pieces
            if (boardy[7][spoty] == 'BLACK'):
                if (player == 'BLACK'):
                    return 1
                else:
                    return -1
                
        # see if there are any pieces left of either color
        whiteyLeft = any('WHITE' in row for row in boardy)
        blackyLeft = any('BLACK' in row for row in boardy)

        # check if it is good if there are no white pieces left
        if not whiteyLeft:
            if (player == 'BLACK'):
                    return 1
            else:
                return -1

        # check if it is good if there are no black pieces left 
        if not blackyLeft:
            if (player == 'WHITE'):
                    return 1
            else:
                return -1

        return 0


    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.

        # start by pulling the board
        boardy = state['board']

        players = ('WHITE', 'BLACK')

        for player in players:
            # we will also get who the other player is
            if (player == 'WHITE'):
                checkySide = 0
                badGuy = "BLACK"
            elif (player == 'BLACK'):
                checkySide = 7
                badGuy = "WHITE"

            # start by checking if player has piece at the other end of the board
            for checkySpot in range(0, 8):
                if (boardy[checkySide][checkySpot] == player):
                    return True
            
            # next, check if there are any opposing pieces left
            oponentLeft = False
            for checkyY in range(0, 8):
                for checkyX in range(0, 8):
                    if (boardy[checkyY][checkyX] == badGuy):
                        oponentLeft = True
                        break

                if oponentLeft:
                    break

            if not oponentLeft:
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
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):

    # start by pulling the board
    boardy = state['board']

    # get the number of pieces remaining
    numMyPiecesLeft = sum(row.count(player) for row in boardy)

    return ((2 * numMyPiecesLeft) + random.random())


def offensive_eval_1(state, player):
    
    # start by pulling the board
    boardy = state['board']

    # next, get the other player
    if (player == 'WHITE'):
        meanPlayer = 'BLACK'
    elif (player == 'BLACK'):
        meanPlayer = 'WHITE'

    # get the number of mean pieces remaining
    numMeanPiecesLeft = sum(row.count(meanPlayer) for row in boardy)
    
    return ((2 * (32 - numMeanPiecesLeft)) + random.random())


def defensive_eval_2(state, player):
    
    # start by pulling the board
    boardy = state['board']
    
    # create an initial score
    score = 0

    if (player == 'WHITE'):
        defensiveSpots = (6, 7)
    else:
        defensiveSpots = (0, 1)

    # check how many defenders are still in their spots
    for row in defensiveSpots:
        for column in range(8):
            if (boardy[row][column] == player):
                score = score + 3

    # add a bonus for the number of pieces still alive
    score = score + sum(row.count(player) for row in boardy)
    
    return (score + random.random())


def offensive_eval_2(state, player):
    # start by pulling the board
    boardy = state['board']
    
    # create an initial score
    score = 0

    # loop through the board
    for row in range(8):
        for column in range(8):
            # check how close the player is to the other side
            if (boardy[row][column] == player):
                if (player == 'WHITE'):
                    score = score + (7 - row)
                else:
                    score = score + row
    
    return (score + random.random())

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
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
