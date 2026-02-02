import random
from .base import GameAlgorithm


class SimpleAvoidAlgorithm(GameAlgorithm):
    """
    Algorithm that picks the direction with the most reachable empty squares.
    Uses flood fill to count open space and avoid dead ends.
    """

    def get_move(self, game_state) -> str:
        current_pos = game_state.my_position
        if current_pos is None:
            return 'up'

        occupied = game_state.get_all_occupied_squares()
        map_size = game_state.map_size

        # Score each direction by counting reachable empty squares
        scores = {}
        for direction in self.DIRECTIONS:
            next_pos = self._get_wrapped_next_pos(current_pos, direction, map_size)

            # Skip if next position is occupied
            if next_pos in occupied:
                scores[direction] = -1
                continue

            # Count reachable squares from this direction
            # Include current_pos as occupied (we'll leave a trail)
            blocked = occupied | {current_pos}
            scores[direction] = self._count_reachable(next_pos, blocked, map_size)

        # Find best score
        best_score = max(scores.values())

        # If all moves are blocked, pick any
        if best_score <= 0:
            return random.choice(self.DIRECTIONS)

        # Pick randomly among best directions
        best_dirs = [d for d, s in scores.items() if s == best_score]
        return random.choice(best_dirs)

    def _get_wrapped_next_pos(self, pos, direction, map_size):
        """Get next position with wrap-around."""
        dx, dy = self.DIRECTION_VECTORS[direction]
        x = (pos[0] + dx) % map_size[0]
        y = (pos[1] + dy) % map_size[1]
        return (x, y)

    def _count_reachable(self, start, occupied, map_size, max_count=100):
        """BFS flood fill to count reachable empty squares."""
        if start in occupied:
            return 0

        visited = {start}
        queue = [start]
        count = 0

        while queue and count < max_count:
            pos = queue.pop(0)
            count += 1

            for direction in self.DIRECTIONS:
                next_pos = self._get_wrapped_next_pos(pos, direction, map_size)

                if next_pos not in visited and next_pos not in occupied:
                    visited.add(next_pos)
                    queue.append(next_pos)

        return count
