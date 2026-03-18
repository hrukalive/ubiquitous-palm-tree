import random
from copy import deepcopy

from numpy.ma.core import true_divide
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

        #list of dict for legal action
        actions = []
        player = state['to_move']
        #White goes up, black goes down
        if player == "WHITE":
            direction = -1
            opponent = "BLACK"
        if player == "BLACK":
            direction = 1
            opponent = "WHITE"
        for r in range(8):
            for c in range(8):
                if state['board'][r][c] == player:
                    if 0 <= r + direction < 8:
                        #move forward
                        if state['board'][r+direction][c] == "EMPTY":
                            actions.append({"from": (r, c), "to": (r+direction, (c))})
                        #check diagonal left
                        if c-1 >= 0 and state['board'][r+direction][c-1] in ["EMPTY", opponent]:
                            actions.append({"from": (r, c), "to": (r+direction, (c-1))})
                        #check diagonal right
                        if c + 1 < 8 and state['board'][r+direction][c+1] in ["EMPTY", opponent]:
                            actions.append({"from": (r, c), "to": (r+direction, (c+1))})
        return actions

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

        #copy of the state
        updated_state = deepcopy(state)
        #variables for the from and to for the board
        x1, y1 = action['from']
        x2, y2 = action['to']
        #checking if current is white
        if updated_state['to_move'] == "WHITE":
            #checking if diagonals are able to be captured
            if updated_state['board'][x2][y2] == "BLACK":
                #if captured, then change previous x,y to be empty, new x,y. to be white, and capture increase
                updated_state['board'][x2][y2] = "WHITE"
                updated_state['captures']['WHITE'] += 1
                updated_state['board'][x1][y1] = "EMPTY"
            else:
                #else only update x,y
                updated_state['board'][x2][y2] = "WHITE"
                updated_state['board'][x1][y1] = "EMPTY"
            #change order to be opposite side
            updated_state['to_move'] = "BLACK"
        #checking if current is black
        elif updated_state['to_move'] == "BLACK":
            # checking if diagonals are able to be captured
            if updated_state['board'][x2][y2] == "WHITE":
                # if captured, then change previous x,y to be empty, new x,y. to be black, and capture increase
                updated_state['board'][x2][y2] = "BLACK"
                updated_state['captures']['BLACK'] += 1
                updated_state['board'][x1][y1] = "EMPTY"
            else:
                # else only update x,y
                updated_state['board'][x2][y2] = "BLACK"
                updated_state['board'][x1][y1] = "EMPTY"
            # change order to be opposite side
            updated_state['to_move'] = "WHITE"

        return updated_state

    def utility(self, state, player):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.

        #At terminal state, the player who it switches to loses, so if it is black, and to_go is black, then black lost
        if state['to_move'] == "BLACK" and player == "WHITE":
            return 100000
        elif state['to_move'] == "BLACK" and player == "BLACK":
            return -100000
        elif state['to_move'] == "WHITE" and player == "BLACK":
            return 100000
        else:
            return -100000

    def terminal_test(self, state):
        ##########################################################################
        #  __   __                  ____          _         _   _
        #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
        #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
        #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
        #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
        # Return True if this is a terminal state, False otherwise.

        #Checking if white has reached the top/Black has reached the bottom
        value = False
        for c in range(8):
            if state['board'][0][c] == "WHITE" or state['board'][7][c] == "BLACK":
                value = True
        #Checking if white has captured all or Black has captured all.
        if state['captures']['WHITE'] == 16 or state['captures']['BLACK'] == 16:
            value = True
        return value

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
    count = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                count += 1
    #based on formula provided
    random_num = random.random()
    return 2 * count + random_num


def offensive_eval_1(state, player):
    count = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] != player and state['board'][r][c] != "EMPTY":
                count += 1
    # based on formula provided
    random_num = random.random()
    return 2 * (32 - count) + random_num

#Because offensive 1 is only focused on capturing enemy pieces, we just need to protect our pieces
#and move towards the goal. It would probably not try to block, as it is more concerned about capturing
#even if it did, moving 1 piece 7 steps forward would be faster than capturing 16 pieces.
#so we can coppy defensive_eval 1 but add moving forward, we can also add if the piece is able to be taken by opponent
#we have the if our piece is about to be taken because it ensures our future actions don't put us in a bad state
def defensive_eval_2(state, player):
    #this variable is for own player piece count
    count = 0
    #this variable is for moving forward
    forward = 0
    #this vairable is for our pieces that are threathned
    threat = 0

    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                #increase based on own pieces
                count +=1
                #increase based on how close to other side
                if player == "WHITE":
                    forward += 8-r
                    #because we are white, opponent is black, check diagonal
                    #our diagonal isn't covered by black, so r-1 cause we are going up
                    if (c - 1 >= 0 and r-1 >= 0 and c + 1 <= 7 )and (state['board'][r-1][c-1] == "BLACK" or state['board'][r-1][c+1] == "BLACK"):
                        threat += 1
                elif player == "BLACK":
                    forward += r
                    # because we are black, opponent is white, check diagonal
                    # our diagonal isn't covered by white, so r+1 cause we are going down
                    if (c - 1 >= 0 and r+1 < 7 and c + 1 <= 7 )and (state['board'][r+1][c-1] == "WHITE" or state['board'][r+1][c+1] == "WHITE"):
                        threat += 1
    #it can be really any number, as long as our piece count is high, and threat is negative and higher than taking
    #because this is defensive, we should be more focused on defending
    random_num = random.random()
    return (10 * count) + (-3 * threat) + (1 * forward) + random_num

#because defensive 1 is only about keeping pieces alive, I just need to go to goal
#the idea of this offensive is to go to goal because defensive will not block
#we reward based on how far they move, and we reward more if they are almost at the endgoal
#we can also just add previous offensive to this list
def offensive_eval_2(state, player):
    #almost winning this variable is for pieces that are 1 near the end-goal
    almost_win = 0
    #forward this variable is each piece that is moving forward, and how much they did
    forward_count = 0
    #count of opponents pieces
    opponent_piece = 0
    #scaning the board
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                if player == "WHITE":
                    #if white, then the piece would be 7-row because white is downwards and has to move up
                    #meaning white would be r-1 for example
                    forward_count += 8-r
                    #check if it is almost at the end for white
                    if r == 1:
                        almost_win += 1
                else:
                    #if black, then black would just be row, because black would need to move down based on list number
                    forward_count += r
                    #check if almost at the end for black
                    if r == 6:
                        almost_win += 1
            elif state['board'][r][c] != player and state['board'][r][c] != "EMPTY":
                    opponent_piece += 1
    random_num = random.random()
    #forward is important, but should not be weighted heavily, at least not being outweighed by almost_win
    #can really be any number
    #I just think that moving forward is better than taking pieces, cause it might be longer
    #and almost winning is gonna be the most important
    #but again, the scale/weights can be any number realistically, depending on if you want more taking or more advancing
    return (5 * forward_count) + (10*almost_win) + (1 * (16-opponent_piece)) + random_num

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
        'board state:': state['board'],
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
