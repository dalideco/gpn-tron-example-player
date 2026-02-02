import random
from .base import GameAlgorithm


class QuadrantAvoidAlgorithm(GameAlgorithm):
    """
    Like SimpleAvoid but on ties, picks direction toward quadrant with most empty space.
    Splits map into 4 quadrants and uses that as tiebreaker.
    """

    def get_move(self, game_state) -> str:
        current_pos = game_state.my_position
        if current_pos is None:
            return 'up'

        occupied = game_state.get_all_occupied_squares()
        map_size = game_state.map_size

        # Score each direction by counting reachable empty squares
        scores = {}
        next_positions = {}
        for direction in self.DIRECTIONS:
            next_pos = self._get_wrapped_next_pos(current_pos, direction, map_size)
            next_positions[direction] = next_pos

            if next_pos in occupied:
                scores[direction] = -1
                continue

            blocked = occupied | {current_pos}
            scores[direction] = self._count_reachable(next_pos, blocked, map_size)

        # Find best score
        best_score = max(scores.values())

        if best_score <= 0:
            return random.choice(self.DIRECTIONS)

        # Get all directions with best score
        best_dirs = [d for d, s in scores.items() if s == best_score]

        # If only one best, return it
        if len(best_dirs) == 1:
            return best_dirs[0]

        # Tiebreaker: pick direction toward quadrant with most empty squares
        quadrant_scores = self._count_quadrant_empty(occupied, map_size)

        # Score each tied direction by which quadrant it moves toward
        dir_quadrant_scores = {}
        for direction in best_dirs:
            next_pos = next_positions[direction]
            quadrant = self._get_quadrant(next_pos, map_size)
            dir_quadrant_scores[direction] = quadrant_scores[quadrant]

        # Pick direction with highest quadrant score
        best_quadrant_score = max(dir_quadrant_scores.values())
        final_dirs = [d for d, s in dir_quadrant_scores.items() if s == best_quadrant_score]

        return random.choice(final_dirs)

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

    def _get_quadrant(self, pos, map_size):
        """
        Return quadrant index (0-3):
        0 = top-left, 1 = top-right, 2 = bottom-left, 3 = bottom-right
        """
        mid_x = map_size[0] // 2
        mid_y = map_size[1] // 2

        if pos[0] < mid_x:
            return 0 if pos[1] < mid_y else 2
        else:
            return 1 if pos[1] < mid_y else 3

    def _count_quadrant_empty(self, occupied, map_size):
        """Count empty squares in each quadrant."""
        mid_x = map_size[0] // 2
        mid_y = map_size[1] // 2

        counts = {0: 0, 1: 0, 2: 0, 3: 0}

        for x in range(map_size[0]):
            for y in range(map_size[1]):
                if (x, y) not in occupied:
                    if x < mid_x:
                        quadrant = 0 if y < mid_y else 2
                    else:
                        quadrant = 1 if y < mid_y else 3
                    counts[quadrant] += 1

        return counts
