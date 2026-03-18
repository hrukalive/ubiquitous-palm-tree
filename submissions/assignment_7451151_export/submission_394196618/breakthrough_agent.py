import time
import math
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
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player)
        if depth == 0:
            return eval_fn(state, player) if eval_fn else game.utility(state, player)

        v = -math.inf
        for action in game.actions(state):
            v = max(v, min_value(game.result(state, action), depth - 1))

        return v

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player)
        if depth == 0:
            return eval_fn(state, player) if eval_fn else game.utility(state, player)

        v = math.inf
        for action in game.actions(state):
            v = min(v, max_value(game.result(state, action), depth - 1))
        return v

    if game.terminal_test(state):
        return None

    elif player == "WHITE":
        plays = []
        for action in game.actions(state):
            plays.append([min_value(game.result(state, action), d-1), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1], expanded_nodes

    elif player == "BLACK":
        plays = []
        for action in game.actions(state):
            plays.append([max_value(game.result(state, action), d-1), action])
        return sorted(plays, key=lambda x: x[0])[0][1], expanded_nodes

    return None


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

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        v = -math.inf
        move = None
        for action in game.actions(state):
            v2, _ = min_value(game.result(state, action), alpha, beta, depth - 1)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        v = math.inf
        move = None
        for action in game.actions(state):
            v2, _ = max_value(game.result(state, action), alpha, beta, depth - 1)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    value, action = max_value(state, -math.inf, math.inf, d)

    return action, expanded_nodes


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
