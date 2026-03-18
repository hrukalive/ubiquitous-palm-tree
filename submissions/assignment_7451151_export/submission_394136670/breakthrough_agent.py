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

    # Remember who started this search — every score is calculated from their point of view
    player = game.to_move(state)

    # This counter goes up by 1 every time we look at a new board position
    expanded_nodes = 0

    def max_value(state, depth):
        # It's our turn — we want the highest possible score
        nonlocal expanded_nodes
        expanded_nodes += 1  # count this board position as visited

        # If the game is already over, return the real win/loss score
        if game.terminal_test(state):
            return game.utility(state, player)

        # If we've looked ahead as far as we're allowed, use the guess function instead
        if depth >= d:
            return eval_fn(state, player)

        # Try every possible move and keep track of the best (highest) score we find
        best = float("-inf")  # start with the worst imaginable score
        for action in game.actions(state):
            next_state = game.result(state, action)  # imagine making this move
            best = max(best, min_value(next_state, depth + 1))  # opponent plays next
        return best

    def min_value(state, depth):
        # It's the opponent's turn — they want the lowest possible score (worst for us)
        nonlocal expanded_nodes
        expanded_nodes += 1  # count this board position as visited

        # If the game is already over, return the real win/loss score
        if game.terminal_test(state):
            return game.utility(state, player)

        # If we've looked ahead as far as we're allowed, use the guess function instead
        if depth >= d:
            return eval_fn(state, player)

        # Try every possible move and keep track of the worst (lowest) score for us
        worst = float("inf")  # start with the best imaginable score (opponent wants to minimize)
        for action in game.actions(state):
            next_state = game.result(state, action)  # imagine the opponent making this move
            worst = min(worst, max_value(next_state, depth + 1))  # we play next
        return worst

    # Now pick the best move from the current position.
    # We try every legal move, score it using min_value (since the opponent moves after us),
    # and keep whichever move gave us the highest score.
    best_action = None
    best_score = float("-inf")  # we haven't seen any move yet, so start with the worst score

    for action in game.actions(state):
        next_state = game.result(state, action)  # imagine making this move
        score = min_value(next_state, 1)         # opponent responds; depth starts at 1
        if score > best_score:
            best_score = score
            best_action = action  # this move is better than anything we've seen so far

    return best_action, expanded_nodes


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

    # Remember who started this search — every score is calculated from their point of view
    player = game.to_move(state)

    # This counter goes up by 1 every time we look at a new board position
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        # It's our turn — we want the highest possible score.
        #
        # alpha = the best score WE are already guaranteed from somewhere earlier in the search.
        #         If we find something better, we update alpha.
        # beta  = the best score the OPPONENT is already guaranteed from somewhere earlier.
        #         If our score ever reaches beta, the opponent will never let us get here,
        #         so we can stop looking (this is called a "beta cutoff").
        nonlocal expanded_nodes
        expanded_nodes += 1  # count this board position as visited

        # If the game is already over, return the real win/loss score
        if game.terminal_test(state):
            return game.utility(state, player)

        # If we've looked ahead as far as we're allowed, use the guess function instead
        if depth >= d:
            return eval_fn(state, player)

        best = float("-inf")  # start with the worst imaginable score
        for action in game.actions(state):
            next_state = game.result(state, action)
            best = max(best, min_value(next_state, alpha, beta, depth + 1))

            # If our score is already >= beta, the opponent will never let us reach this node.
            # No point checking the rest of the moves — skip them (beta cutoff).
            if best >= beta:
                return best

            # Update alpha: we now know we can guarantee at least this score
            alpha = max(alpha, best)

        return best

    def min_value(state, alpha, beta, depth):
        # It's the opponent's turn — they want the lowest possible score (worst for us).
        #
        # alpha = the best score WE are already guaranteed.
        #         If the opponent's score ever drops to alpha or below, WE will never
        #         let the game reach this node, so we can stop (alpha cutoff).
        # beta  = the best score the OPPONENT is already guaranteed.
        #         If we find something worse than beta, we update beta.
        nonlocal expanded_nodes
        expanded_nodes += 1  # count this board position as visited

        # If the game is already over, return the real win/loss score
        if game.terminal_test(state):
            return game.utility(state, player)

        # If we've looked ahead as far as we're allowed, use the guess function instead
        if depth >= d:
            return eval_fn(state, player)

        worst = float("inf")  # start with the best imaginable score (opponent minimizes)
        for action in game.actions(state):
            next_state = game.result(state, action)
            worst = min(worst, max_value(next_state, alpha, beta, depth + 1))

            # If our score is already <= alpha, we would never choose this path.
            # No point checking the rest of the moves — skip them (alpha cutoff).
            if worst <= alpha:
                return worst

            # Update beta: the opponent now knows they can guarantee at most this score
            beta = min(beta, worst)

        return worst

    # Pick the best move from the current position using alpha-beta pruning.
    # alpha and beta start at the most extreme values (no guarantees yet).
    best_action = None
    best_score = float("-inf")
    alpha = float("-inf")  # we have no guarantee yet
    beta = float("inf")    # opponent has no guarantee yet

    for action in game.actions(state):
        next_state = game.result(state, action)
        score = min_value(next_state, alpha, beta, 1)  # opponent responds first
        if score > best_score:
            best_score = score
            best_action = action  # best move found so far

        # Update alpha at the root level too, so later branches can be pruned
        alpha = max(alpha, best_score)

    return best_action, expanded_nodes


##########################################################################


class BaseAgent:
    def __init__(self, name, depth, eval_fn):
        self.name = name          # a label like "AlphaBeta Off1" used in printouts
        self.depth = depth        # how many moves ahead this agent will look
        self.eval_fn = eval_fn    # the function used to score a board when depth runs out
        self.time_per_move = []   # list of how many seconds each move took
        self.nodes_per_move = []  # list of how many board positions each move looked at

    def select_move(self, game, state):
        raise NotImplementedError

    def reset(self):
        # Clear the move history so the agent is ready for a brand new game
        self.time_per_move = []
        self.nodes_per_move = []


class RandomAgent(BaseAgent):
    def __init__(self, name="Random"):
        super().__init__(name, depth=0, eval_fn=None)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        # Just pick a random legal move — no thinking involved
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
        # Use minimax to find the best move, looking self.depth moves ahead
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
        # Use alpha-beta search to find the best move — same idea as minimax but faster
        # because it skips branches that can't possibly affect the final decision
        move, nodes = alpha_beta_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move