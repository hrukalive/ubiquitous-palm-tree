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
        if state['to_move'] in ("WHITE", "BLACK"):
            return state['to_move']
        return None

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

        if not state:
            return None

        board = deepcopy(state['board'])
        player = self.to_move(state)
        legal_actions = list()
        forward_direction = 1 if player == "BLACK" else -1 # Forward moving space for player.
        end_location = 0 if player == "WHITE" else 7 # Calculates the ending position in the y-direction.

        for yi, y in enumerate(board):
            for xi, x in enumerate(y):
                if x == player:
                    # Check legal moves.
                    # The only times the player cant move is if it's at its end or someone is in front.
                    from_loc = (yi, xi)

                    if yi != end_location:
                        for xscan in range(-1, 2, 1):

                            # Check the bounds of xscan to make sure its legal for the piece.
                            if xi + xscan < 0 or xi + xscan > len(board[0]) - 1:
                                continue

                            scan_location = board[yi + forward_direction][xi + xscan]

                            if scan_location == "EMPTY" or (scan_location != player and xscan != 0):
                                legal_actions.append({"from": from_loc, "to": (yi + forward_direction, xi + xscan)})

        return legal_actions


    def result(self, state, action):
        #         # Return the resulting state after applying the action to the current state.
        #         # The action is represented as a dict containing "to_move" (alternating),
        #         #      "captures" (updated captures) and "board" (updated grid).
        #
        #         # 'to_move': "WHITE",  # Player is also a string "WHITE" or "BLACK".
        #         # 'captures': {"WHITE": 0, "BLACK": 0},  # Initially, white and black have captured 0 pieces.
        # 'board': grid.

        if not action:
            return state

        resulting_state = deepcopy(state)
        player = state['to_move']
        next_turn = "WHITE" if player == "BLACK" else "BLACK"
        current_position = action['from']
        next_position = action['to']

        if action in self.actions(state):
            # Void current location.
            resulting_state['board'][current_position[0]][current_position[1]] = "EMPTY"

            # Account for captures for current player.
            if resulting_state['board'][next_position[0]][next_position[1]] == next_turn:
                resulting_state['captures'][player] += 1

            # Move piece.
            resulting_state['board'][next_position[0]][next_position[1]] = player

            # Switch turn (you had this computed but never applied)
            resulting_state['to_move'] = next_turn

        return resulting_state

    def utility(self, state, player):
        board = state['board']  # 8x8, y=0..7 downward, x=0..7 right

        # Collect the pawns y's.
        white_ys = []
        black_ys = []
        for y in range(8):
            for x in range(8):
                v = board[y][x]
                if v == "WHITE":
                    white_ys.append(y)
                elif v == "BLACK":
                    black_ys.append(y)

        # Terminal checks.
        if not black_ys or (0 in white_ys):  # White reached top or black eliminated.
            return 1 if player == "WHITE" else -1
        if not white_ys or (7 in black_ys):  # Black reached bottom or white eliminated.
            return 1 if player == "BLACK" else -1

        # Progress score: "closest pawn to goal"
        white_progress = (7 - min(white_ys)) / 7.0
        black_progress = (max(black_ys)) / 7.0

        if player == "WHITE":
            return white_progress - black_progress
        else:
            return black_progress - white_progress


    def terminal_test(self, state):
        if not state:
            return None

        terminal_rows = state['board'][::len(state['board']) - 1]

        if "BLACK" in terminal_rows[1]:
            return True
        elif "WHITE" in terminal_rows[0]:
            return True
        return False


    def display(self, state):

        if not state: return

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

    pieces_remaining = "\n".join("".join(state['board'][r][c] for c in range(8)) for r in range(8)).count(player)

    return 2 * pieces_remaining + random.random()


def offensive_eval_1(state, player):

    opposing_player = "WHITE" if player == "BLACK" else "BLACK"
    pieces_remaining = "\n".join("".join(state['board'][r][c] for c in range(8)) for r in range(8)).count(opposing_player)
    
    return 2 * (32 - pieces_remaining) + random.random()


def defensive_eval_2(state, player):
    board = state["board"]
    opp = "WHITE" if player == "BLACK" else "BLACK"

    if opp == "WHITE":
        # White is dangerous the closer it gets to row 0
        return -sum(7 - r for r in range(8) for c in range(8)
                    if board[r][c] == "WHITE")
    else:
        # Black is dangerous the closer it gets to row 7
        return -sum(r for r in range(8) for c in range(8)
                    if board[r][c] == "BLACK")


def offensive_eval_2(state, player):
    board = state["board"]
    pressure_rate = 1.22

    alive_eval = (
        [7 - r for r in range(8) for c in range(8) if board[r][c] == "WHITE"]
        if player == "WHITE"
        else [r for r in range(8) for c in range(8) if board[r][c] == "BLACK"]
    )

    if not alive_eval:
        return -float("inf")

    distance_eval = max(alive_eval)  # works for both colors with your alive_eval definition
    return sum(alive_eval) + (distance_eval * pressure_rate)

ag_eval_fn = offensive_eval_2           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = offensive_eval_2  # ⚠️ Change this to your preferred evaluation function for competition.

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
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_2)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=True, progress=True)
    print(results)