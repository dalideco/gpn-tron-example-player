class Player:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
        self.taken_squares = set()
        self.head_position = None  # Current position (last added)

    def add_position(self, x, y):
        self.taken_squares.add((x, y))
        self.head_position = (x, y)

    def print(self):
        print(f"Player {self.username} (ID: {self.player_id}) has taken squares: {self.taken_squares}")
