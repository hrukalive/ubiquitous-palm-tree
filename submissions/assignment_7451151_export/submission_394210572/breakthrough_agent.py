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

        # expand the nodes
        expanded_nodes = expanded_nodes + 1

        # check for a terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        
        # check for the depth
        if (depth == 0):
            return eval_fn(state, player)

        # find the best move!
        value = float('-inf')
        for movey in game.actions(state):
            value = max(value, min_value(game.result(state, movey), (depth - 1)))

        return value

    def min_value(state, depth):
        nonlocal expanded_nodes
        # expand the nodes
        expanded_nodes = expanded_nodes + 1

        # check for a terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        
        # check for the depth
        if (depth == 0):
            return eval_fn(state, player)

        # find the best move!
        value = float('inf')
        for movey in game.actions(state):
            value = min(value, max_value(game.result(state, movey), (depth - 1)))

        return value
    
    # keep track of the best score
    bestScore = float('-inf')
    # keep track of the best move
    bestMovey = None
    
    # start the search
    for movey in game.actions(state):
        value = min_value(game.result(state, movey), (d - 1))
        # if the value is better, record it as the best move!
        if (value > bestScore):
            bestScore = value
            bestMovey = movey

    return bestMovey, expanded_nodes


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
        # expand the nodes
        expanded_nodes = expanded_nodes + 1

        # check for a terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        
        # check for the depth
        if (depth == 0):
            return eval_fn(state, player)

        # find the best move!
        value = float('-inf')
        for movey in game.actions(state):
            value = max(value, min_value(game.result(state, movey), (depth - 1), alpha, beta))
            alpha = max(alpha, value)
            # if alpha is greater than beta, prune!
            if (alpha >= beta):
                break

        return value

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        # expand the nodes
        expanded_nodes = expanded_nodes + 1

        # check for a terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        
        # check for the depth
        if (depth == 0):
            return eval_fn(state, player)

        # find the best move!
        value = float('inf')
        for movey in game.actions(state):
            value = min(value, max_value(game.result(state, movey), (depth - 1), alpha, beta))
            beta = min(beta, value)
            # if alpha is greater than beta, prune!
            if (alpha >= beta):
                break

        return value
    
    # keep track of the best score
    bestScore = float('-inf')
    # keep track of the best move
    bestMovey = None
    # keep track of alpha
    alpha = float('-inf')
    # keep track og beta 
    beta = float('inf')
    
    # start the search
    for movey in game.actions(state):
        value = min_value(game.result(state, movey), (d - 1), alpha, beta)
        # if the value is better, record it as the best move!
        if (value > bestScore):
            bestScore = value
            bestMovey = movey
        # update alpha
        alpha = max(alpha, bestScore)

    return bestMovey, expanded_nodes


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
