import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = game.to_move(state)

    # Provide a safe default eval function
    if eval_fn is None:
            raise ValueError("minimax_cutoff_search needs eval_fn (no default available).")

    expanded_nodes = 0

    def max_value(s, depth):
        nonlocal expanded_nodes
        if game.terminal_test(s):
            return game.utility(s, player), None
        if depth <= 0:
            return eval_fn(s, player), None

        actions = game.actions(s)
        if not actions:
            # No moves: treat as terminal-ish
            return eval_fn(s, player), None

        expanded_nodes += 1  # count expanding this node

        v1 = -np.inf
        move = None
        for a in actions:
            v2, _ = min_value(game.result(s, a), depth - 1)
            if v2 > v1:
                v1, move = v2, a
        return v1, move

    def min_value(s, depth):
        nonlocal expanded_nodes
        if game.terminal_test(s):
            return game.utility(s, player), None
        if depth <= 0:
            return eval_fn(s, player), None

        actions = game.actions(s)
        if not actions:
            return eval_fn(s, player), None

        expanded_nodes += 1  # count expanding this node

        v1 = np.inf
        move = None
        for a in actions:
            v2, _ = max_value(game.result(s, a), depth - 1)
            if v2 < v1:
                v1, move = v2, a
        return v1, move

    value, action = max_value(state, d)
    return action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        if hasattr(game, "eval"):
            eval_fn = game.eval
        else:
            raise ValueError("alpha_beta_cutoff_search needs eval_fn (no default available).")

    def max_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(s):
            return game.utility(s, player), None
        if depth <= 0:
            return eval_fn(s, player), None

        actions = game.actions(s)
        if not actions:
            return eval_fn(s, player), None

        expanded_nodes += 1

        v = -np.inf
        move = None
        for a in actions:
            v2, _ = min_value(game.result(s, a), alpha, beta, depth - 1)
            if v2 > v:
                v, move = v2, a
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, move

    def min_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(s):
            return game.utility(s, player), None
        if depth <= 0:
            return eval_fn(s, player), None

        actions = game.actions(s)
        if not actions:
            return eval_fn(s, player), None

        expanded_nodes += 1

        v = np.inf
        move = None
        for a in actions:
            v2, _ = max_value(game.result(s, a), alpha, beta, depth - 1)
            if v2 < v:
                v, move = v2, a
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, move

    v, a = max_value(state, -np.inf, np.inf, d)
    return a, expanded_nodes


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
