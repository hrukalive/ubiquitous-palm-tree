import time
from os import terminal_size

import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    expanded_nodes = 0
    best_move = None
    best_value = -np.inf

    if game.terminal_test(state): # Game is over
        return None, expanded_nodes

    else:
        possible_moves = game.actions(state)

        for move in possible_moves:

            r = game.result(state, move)
            p = state['to_move']
            max = max_value(game, r, d, p, eval_fn)
            v = max[0]

            if v > best_value:
                best_move = move
                best_value = v

            expanded_nodes += (1 + max[1])

    return best_move, expanded_nodes

def max_value(game, state, depth, original_player, eval_fn=None):

    expanded_nodes_m = 0
    best_value = -np.inf

    if game.terminal_test(state):
        best_value = game.utility(state, original_player) * 1000000

    elif depth == 0:
        best_value = eval_fn(state, original_player)

    else:
        possible_moves = game.actions(state)
        for move in possible_moves:
            expanded_nodes_m += 1
            r = game.result(state, move)
            min = min_value(game, r, depth - 1, original_player, eval_fn)
            v = min[0]
            if v > best_value:
                best_value = v

            expanded_nodes_m += min[1]

    return best_value, expanded_nodes_m

def min_value(game, state, depth, original_player, eval_fn=None):

    expanded_nodes_m = 0
    best_value = +np.inf

    if game.terminal_test(state):
        best_value = game.utility(state, original_player) * 1000000

    elif depth == 0:
        best_value = eval_fn(state, original_player)

    else:
        possible_moves = game.actions(state)
        for move in possible_moves:
            expanded_nodes_m += 1
            r = game.result(state, move)
            max = max_value(game, r, depth - 1, original_player, eval_fn)
            v = max[0]
            if v < best_value:
                best_value = v

            expanded_nodes_m += max[1]

    return best_value, expanded_nodes_m



def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""


    expanded_nodes = 0
    best_move = None
    best_value = -np.inf

    if game.terminal_test(state): # Game is over
        return None, expanded_nodes

    else:
        possible_moves = game.actions(state)

        for move in possible_moves:

            r = game.result(state, move)
            p = state['to_move']
            max = AB_max_value(game, r, d, p, eval_fn, -np.inf, +np.inf)
            v = max[0]

            if v > best_value:
                best_move = move
                best_value = v

            expanded_nodes += (1 + max[1])

    return best_move, expanded_nodes

def AB_max_value(game, state, depth, original_player, eval_fn=None, alpha=None, beta=None):

    expanded_nodes_m = 0
    best_value = -np.inf

    if game.terminal_test(state):
        best_value = game.utility(state, original_player) * 1000000

    elif depth == 0:
        best_value = eval_fn(state, original_player)

    else:
        possible_moves = game.actions(state)
        for move in possible_moves:
            expanded_nodes_m += 1
            r = game.result(state, move)
            min = AB_min_value(game, r, depth - 1, original_player, eval_fn, alpha, beta)
            v = min[0]
            if v > best_value:
                best_value = v
                alpha = max(alpha, best_value)
                if best_value >= beta:
                    return best_value, expanded_nodes_m
            expanded_nodes_m += min[1]


    return best_value, expanded_nodes_m

def AB_min_value(game, state, depth, original_player, eval_fn=None, alpha=None, beta=None):

    expanded_nodes_m = 0
    best_value = +np.inf

    if game.terminal_test(state):
        best_value = game.utility(state, original_player) * 1000000

    elif depth == 0:
        best_value = eval_fn(state, original_player)

    else:
        possible_moves = game.actions(state)
        for move in possible_moves:
            expanded_nodes_m += 1
            r = game.result(state, move)
            max = AB_max_value(game, r, depth - 1, original_player, eval_fn, alpha, beta)
            v = max[0]
            if v < best_value:
                best_value = v
                beta = min(beta, best_value)
                if best_value <= alpha:
                    return best_value, expanded_nodes_m
            expanded_nodes_m += max[1]


    return best_value, expanded_nodes_m

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
