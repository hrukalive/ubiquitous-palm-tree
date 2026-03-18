import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    # Determines whether the game depth is reached or game is over
    def cutoff(state, depth):
        return depth >= d or game.terminal_test(state)

    # Max Node: pick action that maximizes the minimum outcome.
    def max_value(state, depth):
        nonlocal expanded_nodes
        if cutoff(state, depth):
            return eval_fn(state, player)
        val = float("-inf")
        for action in game.actions(state):
            expanded_nodes += 1
            val = max(val, min_value(game.result(state, action), depth + 1))
        return val

    # Min Node: pick action that minimizes the maximum outcome.
    def min_value(state, depth):
        nonlocal expanded_nodes
        if cutoff(state, depth):
            return eval_fn(state, player)
        val = float("inf")
        for a in game.actions(state):
            expanded_nodes += 1
            val = min(val, max_value(game.result(state, a), depth + 1))
        return val

    best_action = None
    best_score = float("-inf")

    # Root decision
    # Chooses action with greatest minimax value
    for a in game.actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), 1)
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

    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    # Determines whether the game depth is reached or game is over
    def cutoff(s, depth):
        return depth >= d or game.terminal_test(s)

    # Prioritizes actions that capture pieces
    def ordered_actions(s):
        acts = game.actions(s)
        opp = "BLACK" if s["to_move"] == "WHITE" else "WHITE"
        acts.sort(key=lambda a: s["board"][a["to"][0]][a["to"][1]] == opp, reverse=True)
        return acts

    # Max Node: Pick move with highest value, prune when v >= beta
    def max_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff(s, depth):
            return eval_fn(s, player)

        v = float("-inf")
        for a in ordered_actions(s):
            expanded_nodes += 1
            v = max(v, min_value(game.result(s, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    # Min node: pick move with lowest value, prune when v <= alpha
    def min_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        if cutoff(s, depth):
            return eval_fn(s, player)

        v = float("inf")
        for a in ordered_actions(s):
            expanded_nodes += 1
            v = min(v, max_value(game.result(s, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    # Root decision: choose action with largest minimax value
    for a in ordered_actions(state):
        expanded_nodes += 1
        score = min_value(game.result(state, a), alpha, beta, 1)
        if score > best_score:
            best_score = score
            best_action = a
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
