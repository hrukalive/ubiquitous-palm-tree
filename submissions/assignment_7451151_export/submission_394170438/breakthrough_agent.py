import time
from cmath import inf

import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    expanded_nodes = 0
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""
    def max_value(state, depth):
        nonlocal expanded_nodes
        if not game.actions(state):
            print("NO LEGAL MOVES but not terminal!")
        actions = game.actions(state)

        if depth == 0 or game.terminal_test(state) or not actions:
            # depth limit reached, or game ended, or no legal actions, use the eval function
            return eval_fn(state, state["to_move"])
        max_so_far = -inf # initially, we have no max so far

        for action_ in actions:
            # simulate actions as the max player
            next_state_ = game.result(state, action_)
            max_so_far = max(max_so_far, min_value(next_state_, depth-1))
            expanded_nodes +=1

        return max_so_far

    def min_value(state, depth):
        nonlocal expanded_nodes
        if not game.actions(state):
            print("NO LEGAL MOVES but not terminal!")
        actions = game.actions(state)
        if depth == 0 or game.terminal_test(state) or not actions:
            # depth limit reached, or game ended, or no legal actions use the eval function
            return eval_fn(state, state["to_move"])

        minimum_so_far = inf # initially, there is no min so far

        for _action_ in actions:
            # simulate actions as the min player
            _next_state_ = game.result(state, _action_)
            minimum_so_far = min(minimum_so_far, max_value(_next_state_, depth-1))
            expanded_nodes +=1

        return minimum_so_far

    # actual start of minimax_cutoff_search(). max and min functions were moved up so they could be called from here

    best_so_far = -inf # initially no best max value
    best_action_so_far = None # no actions initially

    for action in game.actions(state):
        next_state = game.result(state, action) # apply the current action to the current state
        expanded_nodes +=1

        value = min_value(next_state, d-1) # next tree layer is the min player
        if value > best_so_far:
            # update action and best_so_far
            best_so_far = value
            best_action_so_far = action

    return best_action_so_far, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""
    alpha = -9999
    beta = 9999
    expanded_nodes = 0

    def max_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        actions = game.actions(state)
        if depth == 0 or game.terminal_test(state) or not actions:
            # depth limit reached, or game ended, or no legal moves, use the eval function
            return eval_fn(state, state["to_move"])
        max_so_far = -inf  # initially, we have no max so far

        for action_ in actions:
            # simulate actions as the max player
            next_state_ = game.result(state, action_)
            max_so_far = max(max_so_far, min_value(next_state_, depth - 1, alpha, beta))
            if max_so_far >= beta:
                # Don't need to bother checking the other actions/nodes since we already have a better value
                return max_so_far
            expanded_nodes +=1
            alpha = max_so_far

        return max_so_far

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        actions = game.actions(state)
        if depth == 0 or game.terminal_test(state) or not actions :
            # depth limit reached, or game ended, use the eval function
            return eval_fn(state, state["to_move"])

        minimum_so_far = inf  # initially, there is no min so far

        for _action_ in actions:
            # simulate actions as the min player
            _next_state_ = game.result(state, _action_)
            minimum_so_far = min(minimum_so_far, max_value(_next_state_, depth - 1, alpha, beta))
            if minimum_so_far <= alpha:
                # Don't need to bother checking the other nodes since we already have a better value
                return minimum_so_far
            expanded_nodes +=1
            beta = minimum_so_far

        return minimum_so_far

    # actual start of minimax_cutoff_search(). max and min functions were moved up so they could be called from here

    best_so_far = -inf  # initially no best max value
    best_action_so_far = None  # no actions initially

    for action in game.actions(state):
        next_state = game.result(state, action)  # apply the current action to the current state
        expanded_nodes +=1
        value = min_value(next_state, d - 1, alpha, beta)  # next tree layer is the min player
        if value > best_so_far:
            # update action and best_so_far
            best_so_far = value
            best_action_so_far = action

    return best_action_so_far, expanded_nodes


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
