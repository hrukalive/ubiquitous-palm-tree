import time
import numpy as np

# ---------------------------------------------------------------------------
# Adversarial search implementations used by Breakthrough agents:
# - minimax_cutoff_search: baseline depth-limited minimax
# - alpha_beta_cutoff_search: minimax with alpha-beta pruning
# Both return (best_action, expanded_nodes) so experiments can compare speed.
# ---------------------------------------------------------------------------


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

    # Root perspective stays fixed as `player`.
    # max_value/min_value alternate by turn but always score from root player's
    # perspective so comparisons are consistent across plies.

    player = game.to_move(state)
    expanded_nodes = 0

    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    # recursive max_value and min_value alternate by turn
    # track expanded nodes count for performance analysis

    def max_value(s, depth):  # root player is maximizer
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):  # terminal state use game.utility
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = -float("inf")
        acts = game.actions(s)
        if not acts:  # no legal moves before terminal check fallback
            return eval_fn(s, player)

        for a in acts:
            v = max(v, min_value(game.result(s, a), depth - 1))
        return v

    def min_value(s, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = float("inf")
        acts = game.actions(s)
        if not acts:
            return eval_fn(s, player)

        for a in acts:
            v = min(v, max_value(game.result(s, a), depth - 1))
        return v

    best_score = -float("inf")
    best_action = None
    actions = game.actions(state)

    if not actions:
        return None, expanded_nodes

    # Root chooses the action with maximum backed-up minimax score.
    for action in actions:
        score = min_value(game.result(state, action), d - 1)
        if score > best_score:
            best_score = score
            best_action = action

    return best_action, expanded_nodes  # baseline adverarial search without pruning


def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):  # same goal as minimax but faster via pruning
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

    if eval_fn is None:
        eval_fn = lambda s, p: game.utility(s, p)

    def max_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = -float("inf")
        acts = game.actions(s)
        if not acts:
            return eval_fn(s, player)

        for a in acts:
            v = max(v, min_value(game.result(s, a), alpha, beta, depth - 1))
            # Beta cutoff: MIN already has a better option elsewhere.
            if v >= beta:
                return v
            alpha = max(alpha, v)  # MAX's best guaranteed lower bound

        return v

    def min_value(s, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1

        if game.terminal_test(s):
            return game.utility(s, player)
        if depth == 0:
            return eval_fn(s, player)

        v = float("inf")
        acts = game.actions(s)
        if not acts:
            return eval_fn(s, player)

        for a in acts:
            v = min(v, max_value(game.result(s, a), alpha, beta, depth - 1))
            # Alpha cutoff: MAX already has a better option elsewhere.
            if v <= alpha:
                return v
            beta = min(beta, v)  # MIN's best guaranteed upper bound

        return v

    best_action = None
    best_score = -float("inf")
    alpha, beta = -float("inf"), float("inf")
    actions = game.actions(state)

    if not actions:
        return None, expanded_nodes

    # At the root, update alpha as soon as a better move is found so later
    # siblings can be pruned earlier.
    for action in actions:
        score = min_value(game.result(state, action), alpha, beta, d - 1)
        if score > best_score:
            best_score = score
            best_action = action
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
        # Instrumentation is done here (time + expanded nodes) so the search
        # functions stay focused on algorithm logic.
        t0 = time.perf_counter()
        move, nodes = alpha_beta_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move
