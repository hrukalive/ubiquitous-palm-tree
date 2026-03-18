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

    # Pseudo code:
    # player <- game.to_move(state)
    # value, move <- Max-Value(game, state)
    # return move

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        # Pseudo code:
        # function Max_Value(game, state) returns a (utility, move) pair
        #   if game.is_terminal(state) then return game.utility(state, player), null
        #   v <- -inf
        #   for each a in game.Actions(state) do
        #       v2, a2 <- Min_Value(game, game.Result(state, a))
        #       if v2 > v then
        #           v, move <- v2, a
        #   return v, move

        nonlocal expanded_nodes

        if game.terminal_test(state) == True:
            return game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        
        v = float('-inf')
        for a in game.actions(state):
            expanded_nodes += 1
            v2, _ = min_value(game.result(state, a), depth - 1)
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state, depth):
        # Pseudo code:
        # function Min_Value(game, state) returns a (utility, move) pair
        #   if game.is_terminal(state) then return game.utility(state, player), null
        #   v <- +inf
        #   for each a in game.Actions(state) do
        #       v2, a2 <- Max_Value(game, game.Result(state, a))
        #       if v2 < v then
        #           v, move <- v2, a
        #   return v, move
        
        nonlocal expanded_nodes

        if game.terminal_test(state) == True:
            return game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        
        v = float('inf')
        for a in game.actions(state):
            expanded_nodes += 1
            v2, _ = max_value(game.result(state, a), depth - 1)
            if v2 < v:
                v, move = v2, a
        return v, move
    
    _, move = max_value(state, depth=3)
    return move, expanded_nodes


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

    # Pseudo Code:
    # player = game.to_move(state)
    # value, action = max_value(game, state, -inf, +inf)
    # return action
        
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        # Pseudo Code:
        # if state is terminal: return utility
        # initialize v = -inf
        # for each possible action at state:
        #   v' = min_value(successor, a, B)
        #   if v' > v:
        #       v, move = v', action
        #       a = max(a, v)
        #   if v >= B: return v, move
        # return v, move 
        nonlocal expanded_nodes

        if game.terminal_test(state): return game.utility(state, player), None
        elif depth == 0: return eval_fn(state, player), None

        v = float('-inf')
        for a in game.actions(state):
            expanded_nodes += 1
            v2, _ = min_value(game.result(state, a), alpha, beta, depth - 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta: return v, move
        return v, move

    def min_value(state, alpha, beta, depth):
        # Pseudo Code:
        # if state is terminal: return utility
        # initialize v = +inf
        # for each possible action of state:
        #   v' = max_value(successor, a, B)
        #   if v' < v:
        #       v, move = v', action
        #       B = min(B, v)
        #   if v <= a: return v, move
        # return v, move 

        nonlocal expanded_nodes

        if game.terminal_test(state): return game.utility(state, player), None
        elif depth == 0: return eval_fn(state, player), None

        v = float('inf')
        for a in game.actions(state):
            expanded_nodes += 1
            v2, _ = max_value(game.result(state, a), alpha, beta, depth - 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha: return v, move
        return v, move
    
    _, move = max_value(state, float('-inf'), float('inf'), depth=4)
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
