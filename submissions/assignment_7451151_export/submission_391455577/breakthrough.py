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
        player_color = state['to_move']
        grid = state['board']
        for r in range(0, 8):
            for c in range(0, 8):
                if grid[r][c] == player_color:
                    if player_color == "WHITE":
                        if c > 0 and grid[r-1][c-1] != "WHITE":
                            actions.append({"from": (r, c), "to": (r-1, c-1)})
                        elif grid[r-1][c] == "EMPTY":
                            actions.append({"from": (r, c), "to": (r-1, c)})
                        elif c < 7 and grid[r-1][c+1] != "WHITE":
                            actions.append({"from": (r, c), "to": (r-1, c+1)})
                    if player_color == "BLACK":
                        if c > 0 and grid[r+1][c-1] != "BLACK":
                            actions.append({"from": (r, c), "to": (r+1, c-1)})
                        elif grid[r+1][c] == "EMPTY":
                            actions.append({"from": (r, c), "to": (r+1, c)})
                        elif c < 7 and grid[r+1][c+1] != "BLACK":
                            actions.append({"from": (r, c), "to": (r+1, c+1)})

        return actions


    def result(self, state, action):
        # Return the resulting state after applying the action to the current state.
        # The action is represented as a dict containing "to_move" (alternating),
        #      "captures" (updated captures) and "board" (updated grid).
        new_state = deepcopy(state)

        start = action["from"]
        end = action["to"]

        new_state['board'][start[0]][start[1]] = "EMPTY"
        if new_state['board'][end[0]][end[1]] == "WHITE":
            new_state['captures']['BLACK'] += 1
        elif new_state['board'][end[0]][end[1]] == "BLACK":
            new_state['captures']['WHITE'] += 1
        new_state['board'][end[0]][end[1]] = new_state['to_move']
        if new_state['to_move'] == "WHITE":
            new_state['to_move'] = "BLACK"
        else:
            new_state['to_move'] = "WHITE"

        return new_state


    def utility(self, state, player):
        # Return the value to the perspective of the "player";
        #    Positive for win, negative for loss, 0 otherwise.
        if player == "WHITE":
            if state['captures']['WHITE'] == 16 or "WHITE" in state['board'][0]:
                return 1
            elif state['captures']['BLACK'] == 16 or "BLACK" in state['board'][7]:
                return -1
        elif player == "BLACK":
            if state['captures']['BLACK'] == 16 or "BLACK" in state['board'][7]:
                return 1
            elif state['captures']['WHITE'] == 16 or "WHITE" in state['board'][0]:
                return -1

        return 0

    def terminal_test(self, state):
        # Return True if this is a terminal state, False otherwise.
        if state['captures']['WHITE'] == 16  or state['captures']['BLACK'] == 16 or "WHITE" in state['board'][0] or "BLACK" in state['board'][7]:
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
    opposite = "WHITE"
    if player == "WHITE":
        opposite = "BLACK"
    pieces_left = 16 - state['captures'][opposite]

    return 2 * pieces_left + random.random()


def offensive_eval_1(state, player):
    opposite = "WHITE"
    if player == "WHITE":
        opposite = "BLACK"

    opposite_pieces_left = 16 - state['captures'][player]

    return 2 * (32 - opposite_pieces_left) + random.random()


def defensive_eval_2(state, player):
    opposite = "WHITE"
    if player == "WHITE":
        opposite = "BLACK"

    opposite_pieces_left = 16 - state['captures'][player]
    player_pieces_left = 16 - state['captures'][opposite]

    # Adds benefit to being slightly offensive but still prioritizes its own pieces, claims anything that gets too close
    return 2*player_pieces_left - opposite_pieces_left + random.random()


def offensive_eval_2(state, player):
    # This is the evaluation function I wish to enter
    opposite = "WHITE"
    if player == "WHITE":
        opposite = "BLACK"

    opposite_pieces_left = 16 - state['captures'][player]
    player_pieces_left = 16 - state['captures'][opposite]

    furthest_piece = 0
    if player == 'WHITE':
        for r in range(8):
            if player in state['board'][r]:
                furthest_piece = r
    else:
        for r in range(7, -1):
            if player in state['board'][r]:
                furthest_piece = 8 - r

    # Adds utility to having pieces far down the lane to win with the alternate condition, will also make
    # movements to keep the furthest piece safe, as its utility for having a far down piece will be lost
    return (16 - opposite_pieces_left) + (furthest_piece * 2) + random.random()

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
