"""Games or Adversarial Search (Chapter 5)"""

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def initial_state(self):
        """Return the initial state of the game."""
        raise NotImplementedError

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        raise NotImplementedError

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return NotImplementedError

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
    
    def initial_state(self):
        return {"to_move": 'X', "board": {}}

    def to_move(self, state):
        return state["to_move"]

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return [(x, y) for x in range(1, self.h + 1) for y in range(1, self.v + 1) if (x, y) not in state["board"]]

    def result(self, state, action):
        if action not in self.actions(state):
            return state  # Illegal move has no effect
        board = state["board"].copy()
        board[action] = state["to_move"]
        return {
            "to_move": ('O' if self.to_move(state) == 'X' else 'X'),
                "utility": self.compute_utility(board, action, state["to_move"]),
                "board": board
        }
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(self.actions(state)) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, action, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self._k_in_row(board, action, player, (0, 1)) or
                self._k_in_row(board, action, player, (1, 0)) or
                self._k_in_row(board, action, player, (1, -1)) or
                self._k_in_row(board, action, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def _k_in_row(self, board, action, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = action
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = action
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k
