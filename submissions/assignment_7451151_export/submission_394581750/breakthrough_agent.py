import time
import numpy as np

# ---------------------------------------------------------------------------
# Adversarial Search Algorithms
#
# Implements:
# - Depth-limited Minimax
# - Alpha-Beta Pruning
#
# Both return:
# (best_action, expanded_nodes)
#
# Node counts and timing are recorded for experiment comparison.
# ---------------------------------------------------------------------------


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    # Standard depth-limited minimax search.
    # Alternates max and min layers until:
    # - Terminal state
    # - Depth cutoff reached

    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    def max_value(s, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = -float("inf")
        for a in game.actions(s):
            v = max(v, min_value(game.result(s, a), depth - 1))
        return v

    def min_value(s, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = float("inf")
        for a in game.actions(s):
            v = min(v, max_value(game.result(s, a), depth - 1))
        return v

    best_action = None
    best_score = -float("inf")

    for action in game.actions(state):
        score = min_value(game.result(state, action), d - 1)
        if score > best_score:
            best_score = score
            best_action = action

    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    # Alpha-beta pruning search.
    # Uses alpha (best MAX so far) and beta (best MIN so far)
    # to prune branches that cannot influence final decision.

    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    def max_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = -float("inf")
        for a in game.actions(s):
            v = max(v, min_value(game.result(s, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = float("inf")
        for a in game.actions(s):
            v = min(v, max_value(game.result(s, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    best_score = -float("inf")
    alpha, beta = -float("inf"), float("inf")

    for action in game.actions(state):
        score = min_value(game.result(state, action), alpha, beta, d - 1)
        if score > best_score:
            best_score = score
            best_action = action
        alpha = max(alpha, best_score)

    return best_action, expanded_nodes


class BaseAgent:
    # Base agent class.
    # Tracks time per move and nodes expanded per move
    # for reporting and experiment comparison.

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


class MinimaxAgent(BaseAgent):

    def select_move(self, game, state):
        # Executes minimax search and records performance metrics.
        t0 = time.perf_counter()
        move, nodes = minimax_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class AlphaBetaAgent(BaseAgent):

    def select_move(self, game, state):
        # Executes alpha-beta search.
        # Typically expands fewer nodes than minimax at deeper depths.
        t0 = time.perf_counter()
        move, nodes = alpha_beta_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move
