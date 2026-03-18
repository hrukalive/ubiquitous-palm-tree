import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    ##########################################################################
    #  __   __                  ____          _         _   _
    #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
    #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
    #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
    #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        nonlocal expanded_nodes
        if game.terminal_test(state):  # is this state a completed state
            return game.utility(state, player), None

        if depth == d:  # check if the search has reached max depth
            return eval_fn(state, player), None

        max_val = float("-inf")
        best_action = None
        for action in game.actions(state):  #loop through actions
            expanded_nodes += 1
            val, move = min_value(game.result(state, action), depth + 1)
            if val > max_val:  # check if the current action is better than previous
                max_val = val
                best_action = action

        # return best move
        return max_val, best_action

    def min_value(state, depth):
        nonlocal expanded_nodes
        if game.terminal_test(state):  # is this state a completed state
            return game.utility(state, player), None

        if depth == d:  # check if the search has reached max depth
            return eval_fn(state, player), None

        min_val = float("inf")
        best_action = None
        for action in game.actions(state):  #loop through actions
            expanded_nodes += 1
            val, move = max_value(game.result(state, action), depth + 1)
            if val < min_val:  # check if the current action is better than previous
                min_val = val
                best_action = action

        # return best move
        return min_val, best_action

    value, best_action = max_value(state, 0)

    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    ##########################################################################
    #  __   __                  ____          _         _   _
    #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
    #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
    #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
    #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        if game.terminal_test(state):  # is this state a completed state
            return game.utility(state, player), None

        if depth == d:  # check if the search has reached max depth
            return eval_fn(state, player), None

        max_val = float("-inf")
        best_action = None
        for action in game.actions(state):  #loop through actions
            expanded_nodes += 1
            val, move = min_value(game.result(state, action), depth + 1, alpha, beta)

            if val > max_val:  #check for new best state value
                max_val = val
                best_action = action

            if val >= beta:
                return max_val, best_action

            alpha = max(alpha, val)

        return max_val, best_action

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        if game.terminal_test(state):  # is this state a completed state
            return game.utility(state, player), None

        if depth == d:  # check if the search has reached max depth
            return eval_fn(state, player), None

        min_val = float("inf")
        best_action = None
        for action in game.actions(state):
            expanded_nodes += 1
            val, move = max_value(game.result(state, action), depth + 1, alpha, beta)

            if val < min_val:
                min_val = val
                best_action = action

            if val <= alpha:
                return min_val, best_action

            beta = min(beta, val)

        return min_val, best_action

    value, move = max_value(state, 0, float("-inf"), float("inf"))
    return move, expanded_nodes


##########################################################################


class BaseAgent:
    def __init__(self, name, depth, eval_fn):
        self.name = name
        self.depth = depth
        self.eval_fn = eval_fn
        self.time_per_move = []
        self.nodes_per_move = []

    def select_move(self, game, state):
        raise NotImplementedError

    def reset(self):
        self.time_per_move = []
        self.nodes_per_move = []


class RandomAgent(BaseAgent):
    def __init__(self, name="Random"):
        super().__init__(name, depth=0, eval_fn=None)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = np.random.choice(game.actions(state)), 1
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class MinimaxAgent(BaseAgent):
    def __init__(self, name, depth=3, eval_fn=None):
        super().__init__(name, depth, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = minimax_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class AlphaBetaAgent(BaseAgent):
    def __init__(self, name, depth=4, eval_fn=None):
        super().__init__(name, depth, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = alpha_beta_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move
