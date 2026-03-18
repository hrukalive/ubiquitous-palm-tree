import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0


    def max_value(state, depth):
        nonlocal expanded_nodes

        expanded_nodes += 1

        move = None

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        v = float('-inf')

        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), depth - 1)
            if v2 > v:
                v = v2
                move = a

        return v, move

    def min_value(state, depth):
        nonlocal expanded_nodes

        expanded_nodes += 1

        move = None

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        v = float('inf')

        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), depth - 1)
            if v2 < v:
                v = v2
                move = a

        return v, move

    val, action = max_value(state, d)

    return action, expanded_nodes

def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes

        expanded_nodes += 1
        move = None
        v = float('-inf')

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        for a in game.actions(state):
            v2, a2 = min_value(game.result(state, a), alpha, beta, depth - 1)
            if v2 > v:
                v = v2
                move = a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes

        expanded_nodes += 1
        move = None
        v = float('inf')

        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player), None

        for a in game.actions(state):
            v2, a2 = max_value(game.result(state, a), alpha, beta, depth - 1)
            if v2 < v:
                v = v2
                move = a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    val, action = max_value(state, float('-inf'), float('inf'), d)
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
