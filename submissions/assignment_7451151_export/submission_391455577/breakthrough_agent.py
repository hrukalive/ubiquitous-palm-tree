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

        if depth >= d or game.terminal_test(state):
            return None, eval_fn(state, player)

        max_act = None
        max_val = 0

        for i in game.actions(state):
            action, val = min_value(game.result(state, i), depth + 1)
            if max_val < val:
                max_val = val
                max_act = i

        return max_act, max_val


    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if depth >= d or game.terminal_test(state):
            return None, eval_fn(state, player)

        min_act = None
        min_val = float('inf')

        for i in game.actions(state):
            action, val = max_value(game.result(state, i), depth + 1)
            if min_val > val:
                min_val = val
                min_act = i

        return min_act, min_val

    action, val = max_value(state, 0)
    return action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=5, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if depth >= d or game.terminal_test(state):
            return None, eval_fn(state, player)

        max_val = float('-inf')
        max_act = None

        for i in game.actions(state):
            action, val = min_value(game.result(state, i), depth + 1, alpha, beta)

            if max_val < val:
                max_val = val
                max_act = i

            alpha = max(max_val, alpha)

            if alpha >= beta:
                break

        return max_act, max_val

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if depth >= d or game.terminal_test(state):
            return None, eval_fn(state, player)

        min_val = float('inf')
        min_act = None

        for i in game.actions(state):
            action, val = max_value(game.result(state, i), depth + 1, alpha, beta)

            if min_val > val:
                min_val = val
                min_act = i

            beta = min(min_val, beta)

            if beta <= alpha:
                break

        return min_act, min_val

    best_minimax = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')

    for i in game.actions(state):
        act, minimax = min_value(game.result(state, i), 1, alpha, beta)

        if minimax > best_minimax:
            best_minimax = minimax
            best_action = i

        alpha = max(alpha, minimax)

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
