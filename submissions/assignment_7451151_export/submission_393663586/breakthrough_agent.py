import time
import numpy as np
from simplified_state import *


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""
    
    expanded_nodes = 0
    simple_state = simplify_state(state)

    def max_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if terminal_state(state):
            return float('-inf')
        if depth == 0:
            return eval_fn(dict_state(state, "WHITE"))
        return max(min_value(s, depth - 1) for s in expand_white(state))

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if terminal_state(state):
            return float('inf')
        if depth == 0:
            return eval_fn(dict_state(state, "BLACK"))
        return min(max_value(s, depth - 1) for s in expand_black(state))
    
    if game.to_move(state) == "WHITE":
        best_state = max(expand_white(simple_state), key=lambda s: min_value(s, d - 1))
    else:
        best_state = min(expand_black(simple_state), key=lambda s: max_value(s, d - 1))
    
    best_action = action_from_simple_states(simple_state, best_state)
    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    expanded_nodes = 0
    simple_state = simplify_state(state)

    def max_value(state, depth, alpha=float('-inf'), beta=float('inf')):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if terminal_state(state):
            return -1000000
        if depth == 0:
            return eval_fn(dict_state(state, "WHITE"))
        eval = float('-inf')
        for s in expand_white(state):
            eval = max(eval, min_value(s, depth - 1, alpha, beta))
            if eval >= beta:
                return eval
            alpha = max(eval, alpha)
        return eval

    def min_value(state, depth, alpha=float('-inf'), beta=float('inf')):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if terminal_state(state):
            return 1000000
        if depth == 0:
            return eval_fn(dict_state(state, "BLACK"))
        eval = float('inf')
        for s in expand_black(state):
            eval = min(eval, max_value(s, depth - 1, alpha, beta))
            if eval <= alpha:
                return eval
            beta = min(eval, beta)
        return eval
    
    if game.to_move(state) == "WHITE":
        best_state, best_eval = None, float('-inf')
        alpha = float('-inf')
        for s in expand_white(simple_state):
            eval = min_value(s, d - 1, alpha, float('inf'))
            if eval > best_eval:
                best_eval, best_state = eval, s
            alpha = max(alpha, best_eval)
    else:
        best_state, best_eval = None, float('inf')
        beta = float('inf')
        for s in expand_black(simple_state):
            eval = max_value(s, d - 1, float('-inf'), beta)
            if eval < best_eval:
                best_eval, best_state = eval, s
            beta = min(beta, best_eval)
    best_action = action_from_simple_states(simple_state, best_state)
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
