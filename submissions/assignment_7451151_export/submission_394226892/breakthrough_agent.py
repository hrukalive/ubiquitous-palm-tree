import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    ##########################################################################

    player = game.to_move(state)
    if eval_fn is None:
        raise ValueError("eval_fn must be provided for cutoff search.")

    expanded_nodes = 0

    def cutoff_test(s, depth):
        return depth <= 0 or game.terminal_test(s)

    def eval_or_utility(s):
        if game.terminal_test(s):
            # Strongly prefer faster wins / avoid losses at cutoff.
            return 1_000_000 * game.utility(s, player)
        return eval_fn(s, player)

    def max_value(s, depth):
        nonlocal expanded_nodes
        if cutoff_test(s, depth):
            return eval_or_utility(s)
        v = -np.inf
        for a in game.actions(s):
            expanded_nodes += 1
            v = max(v, min_value(game.result(s, a), depth - 1))
        return v

    def min_value(s, depth):
        nonlocal expanded_nodes
        if cutoff_test(s, depth):
            return eval_or_utility(s)
        v = np.inf
        for a in game.actions(s):
            expanded_nodes += 1
            v = min(v, max_value(game.result(s, a), depth - 1))
        return v

    # Choose the action that maximizes the backed-up value.
    best_action = None
    best_score = -np.inf
    for a in game.actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), d - 1)
        if score > best_score or best_action is None:
            best_score = score
            best_action = a

    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    ##########################################################################


    player = game.to_move(state)
    if eval_fn is None:
        raise ValueError("eval_fn must be provided for cutoff search.")

    expanded_nodes = 0

    def cutoff_test(s, depth):
        return depth <= 0 or game.terminal_test(s)

    def eval_or_utility(s):
        if game.terminal_test(s):
            return 1_000_000 * game.utility(s, player)
        return eval_fn(s, player)

    def max_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff_test(s, depth):
            return eval_or_utility(s)
        v = -np.inf
        for a in game.actions(s):
            expanded_nodes += 1
            v = max(v, min_value(game.result(s, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff_test(s, depth):
            return eval_or_utility(s)
        v = np.inf
        for a in game.actions(s):
            expanded_nodes += 1
            v = min(v, max_value(game.result(s, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    best_score = -np.inf
    alpha = -np.inf
    beta = np.inf

    for a in game.actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), alpha, beta, d - 1)
        if score > best_score or best_action is None:
            best_score = score
            best_action = a
        alpha = max(alpha, best_score)

    return best_action, expanded_nodes


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
