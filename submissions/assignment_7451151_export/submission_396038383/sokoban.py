from search import Problem

#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
class Sokoban(Problem):
    """
    A Sokoban problem instance for search algorithms.
    Come up with your own representation for the state.
    """

    def __init__(self, board):
        """
        Initializes the Sokoban problem.
        :param board: List of strings, each string represent a row of the game board
        """
        raise NotImplementedError
        # Remember to call the parent constructor with initial state
        # super().__init__(...)

    def actions(self, state):
        """Returns the list of valid actions from the current state."""
        raise NotImplementedError

    def result(self, state, action):
        """Returns the resulting state after applying the action."""
        raise NotImplementedError

    def is_goal(self, state):
        """Checks if all boxes are on goal positions."""
        raise NotImplementedError

    def h(self, state):
        """Heuristic function for the problem. This should return a
        non-negative estimate of the cost to reach the goal from the
        given state."""
        raise NotImplementedError
