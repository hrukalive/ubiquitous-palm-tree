import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""


    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        raise ValueError("evan_fn must be provided for minimax_cuttoff_search")
    
    def cutoff_test(state, depth):
        return depth == 0 or game.terminal_test(state)
    
    def eval_state(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        return eval_fn(state, player)
    
    def max_value(state, depth):
        nonlocal expanded_nodes
        if cutoff_test(state, depth):
            return eval_state(state)
        
        v = -float("inf")
        for a in game.actions(state):
            expanded_nodes += 1
            v = max(v, min_value(game.result(state, a), depth - 1))
        return v

    def min_value(state, depth):
        nonlocal expanded_nodes
        if cutoff_test(state, depth):
            return eval_state(state)
        
        v = float("inf")
        for a in game.actions(state):
            expanded_nodes += 1
            v = min(v, max_value(game.result(state, a), depth - 1))    
        return v
    
    best_action = None
    best_score = -float("inf")

    for a in game.actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), d-1)
        if score > best_score:
            best_score = score
            best_action = a

    if best_action is None:
        acts = game.actions(state)
        best_action = acts[0] if acts else None

    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        raise ValueError("eval_fn must be provided for alpha_beta_cutoff_search")

    def cutoff_test(state, depth):
        return depth == 0 or game.terminal_test(state)
    
    def eval_state(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        return eval_fn(state, player)

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff_test(state, depth):
            return eval_state(state)

        v = -float("inf")
        for a in game.actions(state):
            expanded_nodes += 1
            v = max(v, min_value(game.result(state, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff_test(state, depth):
            return eval_state(state)

        v = float("inf")
        for a in game.actions(state):
            expanded_nodes += 1
            v = min(v, max_value(game.result(state, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    best_score = -float("inf")
    alpha = -float("inf")
    beta = float("inf")

    for a in game.actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), alpha, beta, d - 1)
        if score > best_score:
            best_score = score
            best_action = a
        alpha = max(alpha, best_score)

    if best_action is None:
        acts = game.actions(state)
        best_action = acts[0] if acts else None

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

