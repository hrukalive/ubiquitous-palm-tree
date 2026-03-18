import time
import numpy as np


def minimax_cutoff_search(game, state, d=2, eval_fn=None):
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

    def min_value(state, depth, a):
        nonlocal expanded_nodes

        if game.terminal_test(state) or depth > d:
            return a, game.utility(state, player)
        v = float('inf')
        min_move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth < d:
                a2, v2 = max_value(state, depth + 1, action)
            else:
                a2, v2 = action, game.utility(state,action) + eval_fn(state, player)
            if v2 < v:
                v, min_move = v2, action
        return min_move, v

    def max_value(state, depth, a):
        nonlocal expanded_nodes
        if game.terminal_test(state) or depth > d:
            return a, game.utility(state,player)
        v = -float('inf')
        max_move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth < d:
                a2, v2 = min_value(state, depth + 1, action)
            else:
                a2, v2 = action, game.utility(state,action) + eval_fn(state, player)
            if v2 > v:
                v, max_move = v2, action
        return max_move, v

    move, util = max_value(state, 0, None)
    return move, expanded_nodes

def alpha_beta_cutoff_search(game, state, d=3, eval_fn=None):
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
    alpha = -float('inf')
    beta = float('inf')

    def min_value(state, depth, a):
        nonlocal expanded_nodes
        nonlocal alpha, beta
        if game.terminal_test(state) or depth > d:
            return a, game.utility(state, player)
        v = float('inf')
        move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth == d:
                a2,v2 = action, game.utility(state,action) + eval_fn(state, player)
            else:
                a2,v2 = max_value(state, depth + 1, action)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return move, v
        return move, v

    def max_value(state, depth, a):
        nonlocal expanded_nodes
        nonlocal alpha, beta
        if game.terminal_test(state) or depth > d:
            return a, game.utility(state, player)
        v = -float('inf')
        move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth == d:
                a2, v2 = action, game.utility(state, action) + eval_fn(state, player)
            else:
                a2, v2 = min_value(state, depth + 1, action)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return move, v
        return move, v


    return max_value(state,0, None)[0], expanded_nodes


def alpha_beta_cutoff_search2(game, state, d=1, eval_fn=None):
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
    alpha = -float('inf')
    beta = float('inf')

    def min_value(state, depth, a):
        nonlocal expanded_nodes
        nonlocal alpha, beta

        if game.terminal_test(state) or depth > d:
            return a, game.utility(state, player)
        v = float('inf')
        min_move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth < d:
                a2, v2 = max_value(state, depth + 1, action)
            else:
                a2, v2 = action, game.utility(state, action) + eval_fn(state, player)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return min_move, v
        return min_move, v

    def max_value(state, depth, a):
        nonlocal expanded_nodes
        nonlocal alpha, beta

        if game.terminal_test(state) or depth > d:
            return a, game.utility(state, player)
        v = -float('inf')
        max_move = None
        actions = game.actions(state)
        expanded_nodes += len(actions)
        for action in actions:
            if depth < d:
                a2, v2 = min_value(state, depth + 1, action)
            else:
                a2, v2 = action, game.utility(state, action) + eval_fn(state, player)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return max_move, v
        return max_move, v


    return max_value(state,0, None)[0], expanded_nodes

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
        nodes = 0
        if len(game.actions(state)) == 0:
            move, nodes = None, 1
        else:
            move, nodes = np.random.choice(game.actions(state)), 1
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class MinimaxAgent(BaseAgent):
    def __init__(self, name, depth=1, eval_fn=None):
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
