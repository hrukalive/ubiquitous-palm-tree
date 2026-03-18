import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    ##########################################################################
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        # If game over
        if game.terminal_test(state):
            return game.utility(state, player), expanded_nodes
        # If we reached max depth
        if depth == d:
            # Return the current game utility + expanded nodes
            return eval_fn(state, player), expanded_nodes

        # Our total actions
        actions = game.actions(state)
        # Decided action
        decided_action = actions[0]
        # Set our theoretical value
        v = float('-inf')

        # For every action we can take from now
        for action in actions:
            # Calculate the minimum value of the next step
            v2, action2 = min_value(game.result(state, action), depth + 1)

            # If the new min is more than the current value
            if v2 > v:
                # Replace our current min
                v, decided_action = v2, action

        return v, decided_action

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        # If game over
        if game.terminal_test(state):
            return game.utility(state, player), expanded_nodes
        # If we reached max depth
        if depth == d:
            # Return the current game utility + expanded nodes
            return eval_fn(state, player), expanded_nodes

        # Our total actions
        actions = game.actions(state)
        # Decided action
        decided_action = actions[0]
        # Set our theoretical value
        v = float('inf')

        # For every action we can take from now
        for action in actions:
            # Calculate the maximum value of the next step
            v2, action2 = max_value(game.result(state, action), depth + 1)

            # If the new max is less than the current value
            if v2 < v:
                # Replace our current min
                v, decided_action = v2, action

        return v, decided_action

    value, move = max_value(state, 1)

    return move, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    ##########################################################################

    player = game.to_move(state)
    expanded_nodes = 0

    # Declare alpha, beta(as global variables)
    # alpha = -np.inf
    # beta = np.inf
    alpha = float("-inf")
    beta = float("inf")

    def max_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1

        # If game over
        if game.terminal_test(state):
            return game.utility(state, player), expanded_nodes
        # If we reached max depth
        if depth >= d:
            # Return the current game utility + expanded nodes
            return eval_fn(state, player), expanded_nodes

        # if 15 in state["captures"].values():
        #     print()
        actions = game.actions(state)
        # if len(actions) == 0:
        #     print()
        # Initialize worst value
        v = float('-inf')
        pick_action = actions[0]

        # Loop through possible actions
        for action in actions:
            # Get our new value
            v_prime, action2 = min_value(game.result(state, action), depth + 1, alpha, beta)

            # If new value is larger than current
            if v_prime > v:
                # Replace current value with new value
                v, pick_action = v_prime, action
                alpha = max(alpha, v)
            # If value is larger/equal to beta
            if v >= beta:
                # Exit out early
                return v, pick_action

        return v, pick_action

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1

        # If game over
        if game.terminal_test(state):
            return game.utility(state, player), expanded_nodes
        # If we reached max depth
        if depth >= d:
            # Return the current game utility + expanded nodes
            return eval_fn(state, player), expanded_nodes

        # if 15 in state["captures"].values():
        #     print()

        actions = game.actions(state)
        # if len(actions) == 0:
        #     print()
        # Initialize worst value
        v = float('inf')
        pick_action = actions[0]

        # Loop through possible actions
        for action in actions:
            # Get our new value
            v_prime, action2 = max_value(game.result(state, action), depth + 1, alpha, beta)

            # If new value is smaller than current
            if v_prime < v:
                # Replace current value with new value
                v, pick_action = v_prime, action
                beta = min(beta, v)
            # If value is smaller/equal to beta
            if v <= alpha:
                # Exit out early
                return v, pick_action

        return v, pick_action

    value, action = max_value(state, 0, alpha, beta)
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
