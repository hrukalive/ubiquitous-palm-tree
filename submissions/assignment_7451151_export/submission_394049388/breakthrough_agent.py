import time
import numpy as np

"""
Part 7:
There are too many moves to calculate start to finish so we have a cutoff
of 3. It simulates the game by taking turns, one layer maximixes one layer minimizes
it. The agent assumes the oppenent plays perfectlly and once a 3-move limit
is reached, we call the custom evaluation function to grade the board and then
pass those grades up to choose the actual move.
"""


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        # check terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        # check depth
        if depth == 0:
            return eval_fn(state, player)

        holder = -float("inf")
        for a in game.actions(state):
            holder = max(holder, min_value(game.result(state, a), depth - 1))

        return holder

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        # check terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        # check depth
        if depth == 0:
            return eval_fn(state, player)

        holder = float("inf")
        for a in game.actions(state):
            holder = min(holder, max_value(game.result(state, a), depth - 1))

        return holder

    # decision making
    best_action = None
    best_score = -float("inf")

    for a in game.actions(state):
        score = min_value(game.result(state, a), d - 1)
        if score > best_score:
            best_score = score
            best_action = a

    return best_action, expanded_nodes


"""
Alpha beta search is essentially a faster minimax, but it does not waste time
calculating bad moves. It keeps track of two numbers, alpha which is the best
score, and beta which is the worst score. If it starts looking down a path and 
discovers the option is worse than what was already found, it prunes it and stops
checking it entirely. This allows teh search to be much more effecient instead
of evaluating usless nodes like minimax. But still finds the exact same 
perfect move minimax would, just faster. 

move to run experiments.py
"""


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1
        # check terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        # check depth
        if depth == 0:
            return eval_fn(state, player)
        holder = -float("inf")
        for a in game.actions(state):
            holder = max(
                holder, min_value(game.result(state, a), depth - 1, alpha, beta)
            )
            # pruning
            if holder >= beta:
                return holder
            # update alpha
            alpha = max(alpha, holder)

        return holder

    def min_value(state, depth, alpha, beta):
        nonlocal expanded_nodes
        expanded_nodes += 1
        # check terminal state
        if game.terminal_test(state):
            return game.utility(state, player)
        # check depth
        if depth == 0:
            return eval_fn(state, player)
        holder = float("inf")
        for a in game.actions(state):
            holder = min(
                holder, max_value(game.result(state, a), depth - 1, alpha, beta)
            )
            # pruning
            if holder <= alpha:
                return holder
            # update beta
            beta = min(beta, holder)

        return holder

    # decision making
    best_action = None
    best_score = -float("inf")
    alpha = -float("inf")
    beta = float("inf")

    # LOOK through all actions
    for a in game.actions(state):
        score = min_value(game.result(state, a), d - 1, alpha, beta)
        if score > best_score:
            best_score = score
            best_action = a
        # update alpha
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
