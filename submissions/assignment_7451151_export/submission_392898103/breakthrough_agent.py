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

        if game.terminal_test(state):
            return game.utility(state, player), None

        if depth == 0:
            return eval_fn(state, player) if eval_fn else 0, None
        
        v = -np.inf
        best_move = None
        for action in game.actions(state):
            expanded_nodes += 1
            # Call min_value with reduced depth
            v2, _ = min_value(game.result(state, action), depth - 1)
            if v2 > v:
                v, best_move = v2, action
        return v, best_move

    def min_value(state, depth):
        nonlocal expanded_nodes
        if game.terminal_test(state):
            return game.utility(state, player), None

        if depth == 0:
            return eval_fn(state, player) if eval_fn else 0, None

        v = np.inf
        best_move = None
        for action in game.actions(state):
            expanded_nodes += 1
            # Call max_value with reduced depth
            v2, _ = max_value(game.result(state, action), depth - 1)
            if v2 < v:
                v, best_move = v2, action
        return v, best_move

    # Start the recursion
    value, move = max_value(state, d)
    return move, expanded_nodes

def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player) if eval_fn else 0, None
        
        v = -np.inf
        best_move = None
        for action in game.actions(state):
            expanded_nodes += 1
            v2, _ = min_value(game.result(state, action), alpha, beta, depth - 1)
            if v2 > v:
                v, best_move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, best_move 
        return v, best_move

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(state):
            return game.utility(state, player), None
        if depth == 0:
            return eval_fn(state, player) if eval_fn else 0, None

        v = np.inf
        best_move = None
        for action in game.actions(state):
            expanded_nodes += 1
            v2, _ = max_value(game.result(state, action), alpha, beta, depth - 1)
            if v2 < v:
                v, best_move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, best_move
        return v, best_move

    value, move = max_value(state, -np.inf, np.inf, d)
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
