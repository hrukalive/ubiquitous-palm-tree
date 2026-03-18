import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):  #returns value and action
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player, depth), None
        elif depth == d:
            return eval_fn(state, player), None #todo change?
        else:
            val = -np.inf
            best_move = None
            for action in game.actions(state):
                new_val, stored_action = min_value(game.result(state, action), depth + 1)
                if new_val > val:
                    val = new_val
                    best_move = action
            return val, best_move

    def min_value(state, depth): #returns value and action
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player, depth), None
        elif depth == d:
            return eval_fn(state, player), None #todo change?
        else:
            val = np.inf
            best_move = None
            for action in game.actions(state):
                new_val, stored_action = max_value(game.result(state, action), depth + 1)
                if new_val < val:
                    val = new_val
                    best_move = action
            return val, best_move

    value, action = max_value(state, 0) #start at d=0
    return action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):  #returns value and action
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player, depth), None
        elif depth == d:
            return eval_fn(state, player), None
        else:
            val = -np.inf
            best_move = None
            for action in game.actions(state):
                new_val, stored_action = min_value(game.result(state, action), alpha, beta, depth + 1)
                if new_val > val:
                    val = new_val
                    best_move = action
                    alpha = max(alpha, val)
                if val >= beta:
                    return val, best_move
            return val, best_move

    def min_value(state, alpha, beta, depth):  #returns value and action
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(state):
            return game.utility(state, player, depth), None
        elif depth == d:
            return eval_fn(state, player), None
        else:
            val = np.inf
            best_move = None
            for action in game.actions(state):
                new_val, stored_action = max_value(game.result(state, action), alpha, beta, depth + 1)
                if new_val < val:
                    val = new_val
                    best_move = action
                    beta = min(beta, val)
                if val <= alpha:
                    return val, best_move
            return val, best_move

    value, action = max_value(state, -np.inf, np.inf, 0)   # start at d=0
    # print("best value and action:", value, action) #TODO REMOVE
    return action, expanded_nodes

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
