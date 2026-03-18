import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class TicTacToe(Game):

    def initial_state(self):
        """
        State is a dict with ONLY:
        - state["board"]: 3x3 list of lists, entries in {"X","O",None}
        - state["to_move"]: "X" or "O"
        """
        return {
            "to_move": "X",
            "board": [[None for _ in range(3)] for _ in range(3)]
        }

    def to_move(self, state):
        return state["to_move"]

    def actions(self, state):
        grid = state["board"]
        actions = []
        for r in range(3):
            for c in range(3):
                if grid[r][c] is None:
                    actions.append((r, c))
        return actions

    def result(self, state, action):
        r, c = action

        if not (0 <= r < 3 and 0 <= c < 3):
            raise ValueError("Move out of bounds")
        if state["board"][r][c] is not None:
            raise ValueError("Illegal move: cell occupied")

        player = state["to_move"]
        new_grid = deepcopy(state["board"])
        new_grid[r][c] = player

        return {
            "to_move": "O" if player == "X" else "X",
            "board": new_grid
        }

    def utility(self, state, player):
        winner = self._winner(state["board"])
        if winner is None:
            return 0
        return 1 if winner == player else -1

    def terminal_test(self, state):
        grid = state["board"]
        return self._winner(grid) is not None or all(
            grid[r][c] is not None
            for r in range(3)
            for c in range(3)
        )

    def display(self, state):
        grid = state["board"]
        for r in range(3):
            row = [
                grid[r][c] if grid[r][c] is not None else "."
                for c in range(3)
            ]
            print(" ".join(row))
        print("to_move:", state["to_move"])
        print()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _winner(self, grid):
        lines = []

        # rows
        for r in range(3):
            lines.append([(r, c) for c in range(3)])

        # columns
        for c in range(3):
            lines.append([(r, c) for r in range(3)])

        # diagonals
        lines.append([(i, i) for i in range(3)])
        lines.append([(i, 2 - i) for i in range(3)])

        for line in lines:
            first = grid[line[0][0]][line[0][1]]
            if first is None:
                continue
            if all(grid[r][c] == first for r, c in line):
                return first

        return None


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
#
# Evaluation functions

def defensive_eval_1(state, player):
    
    
    return ...


def offensive_eval_1(state, player):
    
    
    return ...


def defensive_eval_2(state, player):
    
    
    return ...


def offensive_eval_2(state, player):
    
    
    return ...

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
    game = TicTacToe()

    state = game.initial_state()
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = white_agent.select_move(game, state) if state["to_move"] == "X" else black_agent.select_move(game, state)
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
    # white_captures = state["captures"]["WHITE"]
    # black_captures = state["captures"]["BLACK"]
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
        # 'white_captures': white_captures,
        # 'black_captures': black_captures,
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent, RandomAgent
    game = TicTacToe()
    x_agent = MinimaxAgent("minimax", depth=9)
    o_agent = MinimaxAgent("minimax 2", depth=9)#RandomAgent()
    results = play_game(x_agent, o_agent, max_moves=400, display=True, progress=False)
    print(results)
