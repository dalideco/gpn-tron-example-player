from .player import Player


class GameState:
    """Encapsulates the current state of the game."""

    def __init__(self):
        self._map_size = (0, 0)
        self._players = {}  # player_id -> Player
        self._my_player_id = None

    # --- Properties ---

    @property
    def map_size(self):
        return self._map_size

    @property
    def my_player(self):
        if self._my_player_id is None:
            return None
        return self._players.get(self._my_player_id)

    @property
    def my_position(self):
        """Returns the current head position of my player."""
        if self.my_player:
            return self.my_player.head_position
        return None

    @property
    def opponents(self):
        """Returns list of opponent players."""
        return [p for pid, p in self._players.items() if pid != self._my_player_id]

    @property
    def players(self):
        """Returns dict of all players."""
        return self._players

    # --- Mutation Methods ---

    def start_game(self, width, height, my_player_id):
        """Initialize game with map size and my player ID."""
        self._map_size = (width, height)
        self._my_player_id = my_player_id

    def set_map_size(self, width, height):
        """Set the map dimensions."""
        self._map_size = (width, height)

    def add_player(self, player_id, username):
        """Add a player to the game."""
        player = Player(player_id, username)
        self._players[player_id] = player

    def add_player_position(self, player_id, x, y):
        """Update a player's position."""
        if player_id in self._players:
            self._players[player_id].add_position(x, y)

    def kill_player(self, player_id):
        """Remove a player from the game."""
        if player_id in self._players:
            del self._players[player_id]

    # --- Query Methods ---

    def get_all_occupied_squares(self):
        """Returns set of all squares occupied by any player."""
        occupied = set()
        for player in self._players.values():
            occupied.update(player.taken_squares)
        return occupied

    def wrap_position(self, x, y):
        """Wrap position around the map edges."""
        w, h = self._map_size
        if w == 0 or h == 0:
            return (x, y)
        return (x % w, y % h)

    def is_valid_position(self, x, y):
        """Checks if a position is not occupied (wraps around edges)."""
        wrapped = self.wrap_position(x, y)
        if wrapped in self.get_all_occupied_squares():
            return False
        return True
