import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""
    player = game.to_move(state)
    expanded_nodes = 0

    #make sure there is an evaluation function
    if eval_fn is None:
        eval_fn = game.utility

    #Max and Min functions for minimax with a cutoff depth
    def max_minimax(state, depth):
        #base case (terminal state, or ran out of depth)
        if game.terminal_test(state):
            # this is not an efficient way to do this
            # but is required since the eval_fn implemented does not know what a win is
            return 1000 * game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        #find max move
        value = -9999
        best_move = None
        for move in game.actions(state):
            #keep track of number of expanded nodes
            nonlocal expanded_nodes
            expanded_nodes += 1
            new_value, tmp = min_minimax(game.result(state, move), depth-1)
            if new_value > value:
                value = new_value
                best_move = move
        #all possible moves have been explored
        return value, best_move
    def min_minimax(state, depth):
        #base case (terminal state, or ran out of depth)
        if game.terminal_test(state):
            #this is not an efficient way to do this
            #but is required since the eval_fn implemented does not know what a win is
            return 1000 * game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        #find min move
        value = 9999
        best_move = None
        for move in game.actions(state):
            #keep track of number of expanded nodes
            nonlocal expanded_nodes
            expanded_nodes += 1
            new_value, tmp = min_minimax(game.result(state, move), depth-1)
            if new_value < value:
                value = new_value
                best_move = move
        # all possible moves have been explored
        return value, best_move

    value, move = max_minimax(state, d)

    return move, expanded_nodes


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""
    player = game.to_move(state)
    expanded_nodes = 0

    #make sure there is an evaluation function
    if eval_fn is None:
        eval_fn = game.utility

    # Max and Min functions for minimax with a cutoff depth and alpha beta pruning
    # Max updates alpha when doing alpha beta pruning
    def max_minimax(state, depth, alpha = -9999, beta = 9999):
        # base case (terminal state, or ran out of depth)
        if game.terminal_test(state):
            # this is not an efficient way to do this
            # but is required since the eval_fn implemented does not know what a win is
            return 1000 * game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        # find max move
        value = -9999
        best_move = None
        for move in game.actions(state):
            # keep track of number of expanded nodes
            nonlocal expanded_nodes
            expanded_nodes += 1
            new_value, tmp = min_minimax(game.result(state, move), depth - 1, alpha, beta)
            #otherwise find max
            if new_value > value:
                value = new_value
                best_move = move
                #update alpha in max
                alpha = max(alpha, value)
            #alpha-beta pruning
            if value >= beta:
                return value, best_move
        # all possible moves have been explored so return best
        return value, best_move

    # Min updates beta when doing alpha beta pruning
    def min_minimax(state, depth, alpha=-9999, beta=9999):
        # base case (terminal state, or ran out of depth)
        if game.terminal_test(state):
            # this is not an efficient way to do this
            # but is required since the eval_fn implemented does not know what a win is
            return 1000 * game.utility(state, player), None
        elif depth == 0:
            return eval_fn(state, player), None
        # find max move
        value = 9999
        best_move = None
        for move in game.actions(state):
            # keep track of number of expanded nodes
            nonlocal expanded_nodes
            expanded_nodes += 1
            new_value, tmp = max_minimax(game.result(state, move), depth - 1, alpha, beta)
            # otherwise find min
            if new_value < value:
                value = new_value
                best_move = move
                # update beta in min
                beta = min(beta, value)
            # alpha-beta pruning
            if value <= alpha:
                return value, best_move
        # all possible moves have been explored so return best
        return value, best_move

    value, move = max_minimax(state, d)

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
