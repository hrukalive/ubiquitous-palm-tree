import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    ##########################################################################
    #  __   __                  ____          _         _   _
    #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
    #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
    #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
    #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
    if game.terminal_test(state):
        return {'from': (0,0), 'to': (0,0)}, 0

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        if game.terminal_test(state):
            return {'from': (0, 0), 'to': (0, 0)}, 0
        nonlocal expanded_nodes
        actions = game.actions(state)
        max_eval = float('-inf')
        chosen_action = None
        if depth==1:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = eval_fn(result, player)
                if val > max_eval:
                    max_eval = val
                    chosen_action = action
        else:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                min_val = min_value(result, depth - 1)
                if min_val[1] > max_eval:
                    max_eval = min_val[1]
                    chosen_action = action

        return chosen_action, max_eval

    def min_value(state, depth):
        if game.terminal_test(state):
            return {'from': (0, 0), 'to': (0, 0)}, 0
        nonlocal expanded_nodes
        actions = game.actions(state)
        min_eval = float('inf')
        chosen_action = None
        if depth == 1:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = eval_fn(result, player)
                if val < min_eval:
                    min_eval = val
                    chosen_action = action
        else:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                min_val = min_value(result, depth - 1)[1]
                if min_val < min_eval:
                    min_eval = min_val
                    chosen_action = action
        return chosen_action, min_eval


    action = max_value(state, d)[0]

    return action, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    ##########################################################################
    #  __   __                  ____          _         _   _
    #  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
    #   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
    #    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
    #    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
    if game.terminal_test(state):
        return {'from': (0, 0), 'to': (0, 0)}, 0

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        if game.terminal_test(state):
            return {'from': (0, 0), 'to': (0, 0)}, 0
        nonlocal expanded_nodes
        actions = game.actions(state)
        chosen_action = None
        chosen_val = float('-inf')
        if depth==1:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = game.utility(result, player) + eval_fn(result, player)
                if val > chosen_val:
                    chosen_val = val
                    chosen_action = action
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    break
        else:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = min_value(result, alpha, beta, depth-1)[1]
                if val > chosen_val:
                    chosen_val = val
                    chosen_action = action
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    break
        return chosen_action, chosen_val

    def min_value(state, alpha, beta, depth):
        if game.terminal_test(state):
            return {'from': (0, 0), 'to': (0, 0)}, 0
        nonlocal expanded_nodes
        actions = game.actions(state)
        chosen_action = None
        chosen_val = float('inf')
        if depth == 1:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = game.utility(result, player) + eval_fn(result, player)
                if val < chosen_val:
                    chosen_val = val
                    chosen_action = action
                if val < beta:
                    beta = val
                if alpha >= beta:
                    break
        else:
            for action in actions:
                expanded_nodes += 1
                result = game.result(state, action)
                val = max_value(result, alpha, beta, depth-1)[1]
                if val < chosen_val:
                    chosen_val = val
                    chosen_action = action
                if val < beta:
                    beta = val
                if alpha >= beta:
                    break
        return chosen_action, chosen_val

    action = max_value(state, float('-inf'), float('inf'), d)[0]

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
