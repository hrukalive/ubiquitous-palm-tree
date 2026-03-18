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
        if game.terminal_test(state) or depth == 0:
            return eval_fn(state, player)
        
        v = float('-inf')
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth - 1))
        return v

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth == 0:
            return eval_fn(state, player)
        
        v = float('inf')
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth - 1))
        return v

    # Root of the search: find the action that leads to the highest min_value
    best_score = float('-inf')
    best_action = None
    
    actions = game.actions(state)
    if not actions:
        return None, expanded_nodes

    for a in actions:
        val = min_value(game.result(state, a), d - 1)
        if val > best_score:
            best_score = val
            best_action = a
            
    return best_action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth == 0:
            return eval_fn(state, player)
        
        v = float('-inf')
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth == 0:
            return eval_fn(state, player)
        
        v = float('inf')
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Root level logic
    best_score = float('-inf')
    beta = float('inf')
    best_action = None
    
    actions = game.actions(state)
    if not actions:
        return None, expanded_nodes

    for a in actions:
        # We call min_value because the root is essentially a "max" node
        val = min_value(game.result(state, a), best_score, beta, d - 1)
        if val > best_score:
            best_score = val
            best_action = a
            
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
        # Use np.random.randint since choice doesn't always handle list of dicts well
        actions = game.actions(state)
        move, nodes = actions[np.random.randint(len(actions))], 1
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