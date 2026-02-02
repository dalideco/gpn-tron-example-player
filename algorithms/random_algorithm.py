import random
from .base import GameAlgorithm


class RandomAlgorithm(GameAlgorithm):
    """
    Simple algorithm that picks a random valid move.
    Falls back to any random move if no valid moves exist.
    """

    def get_move(self, game_state) -> str:
        valid_moves = self.get_valid_moves(game_state)

        if valid_moves:
            return random.choice(valid_moves)

        # No valid moves, pick random (will die anyway)
        return random.choice(self.DIRECTIONS)
