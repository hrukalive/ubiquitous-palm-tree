import time
import numpy as np

def order_actions(game, state, actions):
    """Sorts actions to maximize pruning efficiency."""
    player = state['to_move']
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    grid = state['board']
    
    def move_score(action):
        r_from, c_from = action["from"]
        r_to, c_to = action["to"]
        score = 0
        
        if grid[r_to][c_to] == opponent:
            score += 100
            
        dist = (7 - r_to) if player == "WHITE" else r_to
        score += dist * 10
        
        score += (3.5 - abs(c_to - 3.5)) * 2
        
        return score

    return sorted(actions, key=move_score, reverse=True)

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
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        # Cutoff test: terminal state or depth reached
        if game.terminal_test(state) or depth >= d:
            return eval_fn(state, player)
        
        v = -float('inf')
        for action in game.actions(state):
            v = max(v, min_value(game.result(state, action), depth + 1))
        return v

    def min_value(state, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth >= d:
            return eval_fn(state, player)
        
        v = float('inf')
        for action in game.actions(state):
            v = min(v, max_value(game.result(state, action), depth + 1))
        return v

    best_score = -float('inf')
    best_action = None
    
    for action in game.actions(state):
        val = min_value(game.result(state, action), 1)
        if val > best_score:
            best_score = val
            best_action = action
            
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

    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth >= d:
            return eval_fn(state, player)
        
        v = -float('inf')
        # Apply move ordering here
        actions = order_actions(game, state, game.actions(state))
        
        for action in actions:
            v = max(v, min_value(game.result(state, action), alpha, beta, depth + 1))
            if v >= beta:
                return v # Pruning
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        nonlocal expanded_nodes
        expanded_nodes += 1
        if game.terminal_test(state) or depth >= d:
            return eval_fn(state, player)
        
        v = float('inf')
        # Apply move ordering here
        actions = order_actions(game, state, game.actions(state))
        
        for action in actions:
            v = min(v, max_value(game.result(state, action), alpha, beta, depth + 1))
            if v <= alpha:
                return v # Pruning
            beta = min(beta, v)
        return v

    # Root search
    best_score = -float('inf')
    beta = float('inf')
    best_action = None
    
    actions = order_actions(game, state, game.actions(state))
    for action in actions:
        val = min_value(game.result(state, action), best_score, beta, 1)
        if val > best_score:
            best_score = val
            best_action = action
            
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
