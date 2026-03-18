import time
from cmath import inf

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

    #
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        nonlocal expanded_nodes
        #score
        score = -inf

        # depth limit reached
        if depth == 0:
            return eval_fn(state, player)
        #If game is over
        if game.terminal_test(state):
            return game.utility(state, player)

        #For each possible move, apply move to get new state, ask min, if score better than current
        expanded_nodes += 1
        for action in game.actions(state):
            next_state = game.result(state, action)
            x = min_value(next_state, depth-1)
            if x > score:
                score = x
        return score

    def min_value(state, depth):
        nonlocal expanded_nodes
        # score
        score = inf

        # if depth limit reached
        if depth == 0:
            return eval_fn(state, player)
        # if game over
        if game.terminal_test(state):
            return game.utility(state, player)

        # For each possible move, apply move to get new state, ask max, if score worse than current
        expanded_nodes += 1
        for action in game.actions(state):
            next_state = game.result(state, action)
            x = max_value(next_state, depth - 1)
            if x < score:
                score = x
        return score

    #calling first
    best_move = None
    best_score = -inf
    # for each move, ask min, as we are max, to get the best moves
    for action in game.actions(state):
        next_state = game.result(state, action)
        value = min_value(next_state, depth=d)
        if value > best_score:
            best_move = action
            best_score = value
    return best_move, expanded_nodes


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

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        # score
        score = -inf

        # depth limit reached
        if depth == 0:
            return eval_fn(state, player)
        # If game is over
        if game.terminal_test(state):
            return game.utility(state, player)

        #loop through each action
        expanded_nodes += 1
        for action in game.actions(state):
            next_state = game.result(state, action)
            score1 = min_value(next_state, alpha, beta, depth-1)
            if score1 >  score:
                #if bigger than the next, update score
                score = score1
            if score >= beta:
                #pruning here, if score is greater than the beta or the min, the min would not allow it
                return score
            alpha = max(alpha, score)

        return score

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        # score
        score = inf

        # depth limit reached
        if depth == 0:
            return eval_fn(state, player)
        # If game is over
        if game.terminal_test(state):
            return game.utility(state, player)

        # loop through each action
        expanded_nodes += 1
        for action in game.actions(state):
            next_state = game.result(state, action)
            score1 = max_value(next_state, alpha, beta, depth - 1)
            if score1 < score:
                #if less than the next state, update
                score = score1
            if score <= alpha:
                # pruning here, if score is smaller than the alpha or the max, the max would not choose it
                return score
            beta = min(beta, score)

        return score

    best_move = None
    best_score = -inf
    alpha = -inf
    beta = inf

    #calling first
    for action in game.actions(state):
        new_state = game.result(state, action)
        score = min_value(new_state, alpha, beta, d-1)
        #we are in the mind of max, so we do the same for the max_value, where we compare against possibe mins
        if score > best_score:
            best_score = score
            best_move = action
        #update the new alpha, so every future relies on this
        alpha = max(alpha, best_score)


    return best_move, expanded_nodes


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
