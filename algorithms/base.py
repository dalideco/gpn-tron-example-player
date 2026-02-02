from abc import ABC, abstractmethod


class GameAlgorithm(ABC):
    """
    Abstract base class for game movement algorithms.

    Inherit from this class and implement the `get_move` method
    to create a new movement strategy.
    """

    # Valid move directions
    DIRECTIONS = ['up', 'down', 'left', 'right']

    # Direction vectors: direction -> (dx, dy)
    DIRECTION_VECTORS = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0),
    }

    @abstractmethod
    def get_move(self, game_state) -> str:
        """
        Determine the next move based on the current game state.

        Args:
            game_state: GameState object containing map size, players, positions

        Returns:
            str: One of 'up', 'down', 'left', 'right'
        """
        pass

    def get_next_position(self, current_pos, direction):
        """
        Calculate the next position given current position and direction.

        Args:
            current_pos: Tuple (x, y) of current position
            direction: One of 'up', 'down', 'left', 'right'

        Returns:
            Tuple (x, y) of next position
        """
        if current_pos is None:
            return None
        dx, dy = self.DIRECTION_VECTORS[direction]
        return (current_pos[0] + dx, current_pos[1] + dy)

    def get_valid_moves(self, game_state):
        """
        Get list of valid moves from current position.

        Args:
            game_state: GameState object

        Returns:
            List of valid direction strings
        """
        current_pos = game_state.my_position
        if current_pos is None:
            return self.DIRECTIONS.copy()

        valid = []
        for direction in self.DIRECTIONS:
            next_pos = self.get_next_position(current_pos, direction)
            if game_state.is_valid_position(next_pos[0], next_pos[1]):
                valid.append(direction)
        return valid
