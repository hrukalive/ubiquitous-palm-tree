# Rohan Gladson
# IP 2: Playing Breakthrough
# CS 4341: Introduction to Artificial Intelligence


import time
import numpy as np

def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    # Conditional put in place incase we are not provided an
    # eval function, and if that were the case we would simply
    # fall back to a simple utility-based evaluation.
    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    def max_value(state, depth):
        # Return the max utility value achievable from state s.
        nonlocal expanded_nodes

        # Stop if game over: true utility is known
        if game.terminal_test(state):
            return game.utility(state, player)

        # Stop if cutoff reached: estimate with evaluation function
        if depth >= d:
            return eval_fn(state, player)

        # Expand this node (generate successors)
        expanded_nodes += 1
        v = float("-inf")

        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth + 1))

        return v

    def min_value(state, depth):
        # Return the min utility value achievable from state s.
        nonlocal expanded_nodes

        # Stop if game over: true utility is known
        if game.terminal_test(state):
            return game.utility(state, player)

        # Stop if cutoff reached: estimate with evaluation function
        if depth >= d:
            return eval_fn(state, player)

        # Expand this node (generate successors)
        expanded_nodes += 1
        v = float("inf")

        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth + 1))

        return v

    # Root decision: choose the action that maximizes the value
    best_action = None
    best_score = float("-inf")

    # Expanding the root counts too (we are generating its children)
    expanded_nodes += 1
    for a in game.actions(state):
        score = min_value(game.result(state, a), depth=1)
        if score > best_score:
            best_score = score
            best_action = a

    return best_action, expanded_nodes

def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    # Safety fallback if eval_fn is not provided
    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    def max_value(state, alpha, beta, depth):
        # MAX node: current side to move is trying to maximize
        # root player's outcome
        nonlocal expanded_nodes

        # Terminal state: return true outcome
        if game.terminal_test(state):
            return game.utility(state, player)

        # Depth cutoff: estimate value with eval function
        if depth >= d:
            return eval_fn(state, player)

        # Expand node (generate all legal moves)
        expanded_nodes += 1
        v = float("-inf")

        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))

            # Alpha-beta pruning:
            # If MAX has found a value >= beta, MIN will never allow this branch,
            # so we can stop exploring remaining actions.
            if v >= beta:
                return v

            # Update alpha (best value found so far for MAX)
            alpha = max(alpha, v)

        return v

    def min_value(state, alpha, beta, depth):
        # MIN node: opponent tries to minimize root player's outcome
        nonlocal expanded_nodes

        if game.terminal_test(state):
            return game.utility(state, player)

        if depth >= d:
            return eval_fn(state, player)

        expanded_nodes += 1
        v = float("inf")

        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))

            # Alpha-beta pruning:
            # If MIN has found a value <= alpha, MAX will never allow this branch,
            # so we can stop exploring remaining actions.
            if v <= alpha:
                return v

            # Update beta (best value found so far for MIN)
            beta = min(beta, v)

        return v

    # Root decision: choose action that maximizes the alpha-beta value
    best_action = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    # Expanding the root counts as expanding a node
    expanded_nodes += 1
    for a in game.actions(state):
        score = min_value(game.result(state, a), alpha, beta, depth=1)
        if score > best_score:
            best_score = score
            best_action = a

        # Update alpha at the root based on best_score so far
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
