import random
import copy

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
        list_possible_moves = []
        grid = state['board']
        color = state['to_move']
        # determine if we are moving up or down, up is -, down is +
        direction = 0
        if color == "WHITE":
            direction = -1
        else:
            direction = 1
        #check each square in the grid for possible moves
        for row in range(8):
            for col in range(8):
                #if there is a piece that matches the current players color
                if grid[row][col] == color:
                    #check each of the valid moves
                    #check leftmost move
                    if 0 <= row + direction <= 7 and 0 <= col - 1 <= 7:
                        if grid[row + direction][col - 1] != color:
                            #create a dict with "from", "to" tuples
                            move = {
                                "from": (row, col),
                                "to": (row + direction, col - 1)
                            }
                            #save it as a possible move
                            list_possible_moves.append(move)
                    #check middle move
                    if 0 <= row + direction <= 7:
                        if grid[row + direction][col] == "EMPTY":
                            # create a dict with "from", "to" tuples
                            move = {
                                "from": (row, col),
                                "to": (row + direction, col)
                            }
                            # save it as a possible move
                            list_possible_moves.append(move)
                    # check rightmost move
                    if 0 <= row + direction <= 7 and 0 <= col + 1 <= 7:
                        if grid[row + direction][col + 1] != color:
                            # create a dict with "from", "to" tuples
                            move = {
                                "from": (row, col),
                                "to": (row + direction, col + 1)
                            }
                            # save it as a possible move
                            list_possible_moves.append(move)
        return list_possible_moves



    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        color = state['to_move']
        if color == "WHITE":
            new_to_move = "BLACK"
        else:
            new_to_move = "WHITE"
        new_captures = copy.deepcopy(state['captures'])
        new_grid = copy.deepcopy(state['board'])

        #Move the piece
        from_row, from_col = action["from"]
        to_row, to_col = action["to"]
        new_grid[from_row][from_col] = "EMPTY"
        #If we did not move into an empty space we captured a piece
        if new_grid[to_row][to_col] != "EMPTY":
            new_captures[color] = new_captures[color] + 1
        new_grid[to_row][to_col] = color

        to_return = {
            'to_move': new_to_move,  # Player is also a string "WHITE" or "BLACK".
            'captures': new_captures,  # Initially, white and black have captured 0 pieces.
            'board': new_grid,  # 8x8 grid representing the board.
        }  # ⚠️ You must use this structure for the state representation.

        return to_return


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if player == "WHITE":
            team = 1
        else:
            team = -1
        grid = state['board']

        #check white win
        for col in range(8):
            if grid[0][col] == "WHITE":
                return team
        #check black win
        for col in range(8):
            if grid[7][col] == "BLACK":
                return -team
        #check player elimination
        count_white_pieces = 0
        count_black_pieces = 0
        for row in range(8):
            for col in range(8):
                if grid[row][col] == "WHITE":
                    count_white_pieces += 1
                elif grid[row][col] == "BLACK":
                    count_black_pieces += 1
        if count_white_pieces == 0:
            return -team
        if count_black_pieces == 0:
            return team
        #no players won or were eliminated
        return 0

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        return self.utility(state, state['to_move']) != 0

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
    #Return 2 * (number_of_own_pieces_remaining) + random().
    number_of_own_pieces_remaining = 0
    grid =  state['board']
    for row in range(8):
        for col in range(8):
            if grid[row][col] == player:
                number_of_own_pieces_remaining += 1
    return (2 * number_of_own_pieces_remaining) + random.random()


def offensive_eval_1(state, player):
    #Return 2 * (32 - number_of_opponent_pieces_remaining) + random().
    number_of_opponent_pieces_remaining = 0
    grid = state['board']
    if player == "WHITE":
        opponent = "BLACK"
    else:
        opponent = "WHITE"
    for row in range(8):
        for col in range(8):
            if grid[row][col] == opponent:
                number_of_opponent_pieces_remaining += 1
    return (2 * (32 - number_of_opponent_pieces_remaining)) + random.random()

#This has been wining against defensive_eval_1 when testing
#It is really cool how it is meeting expectations of inflicting Pyrrhic victories
#(by that I mean taking pieces when it will lose a piece anyways)
def defensive_eval_2(state, player):
    number_of_own_pieces_remaining = 0
    number_of_opponent_pieces_remaining = 0
    squares_lost_score = 0
    grid = state['board']
    if player == "WHITE":
        opponent = "BLACK"
        square_modifier = 0
    else:
        opponent = "WHITE"
        square_modifier = 7
    # Count number of own pieces remaining
    for row in range(8):
        for col in range(8):
            if grid[row][col] == player:
                number_of_own_pieces_remaining += 1
            #count how far opponents are up on the board
            #(calculate number as well even if not used because it is not defensive then)
            elif grid[row][col] == opponent:
                number_of_opponent_pieces_remaining += 1
                #Square it to make opponents further up on the board worse
                squares_lost_score += abs((row - square_modifier)/4) ** 2

    return 10 * number_of_own_pieces_remaining - squares_lost_score + random.random()/10


#This has been winning against offensive_eval_1 when testing
#I was concerned that it push pieces to far forward because of the squares_taken_score
#But that score requires a piece remaining, so I think it is adding some degree of self-preservation
#And therefore not sacrificing pieces just to take one of the opponents unless there is also another benefit
def offensive_eval_2(state, player):
    number_of_own_pieces_remaining = 0
    number_of_opponent_pieces_remaining = 0
    squares_taken_score = 0
    grid = state['board']
    if player == "WHITE":
        opponent = "BLACK"
        square_modifier = 0
    else:
        opponent = "WHITE"
        square_modifier = 7
    # Count number of own pieces remaining
    for row in range(8):
        for col in range(8):
            if grid[row][col] == player:
                number_of_own_pieces_remaining += 1
                # Square it to make pieces further up on the board better
                squares_taken_score += abs((row - square_modifier) / 4) ** 2
            # count how far opponents are up on the board
            # (calculate number as well even if not used because it is not defensive then)
            elif grid[row][col] == opponent:
                number_of_opponent_pieces_remaining += 1
    return 10 * (32 - number_of_opponent_pieces_remaining) + squares_taken_score + random.random()/10


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
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent, RandomAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)
