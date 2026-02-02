import argparse
import time
from game import GameState
from connect import GameClient
from algorithms import GameAlgorithm, RandomAlgorithm, SimpleAvoidAlgorithm, QuadrantAvoidAlgorithm


ALGORITHMS = {
    'random': RandomAlgorithm,
    'avoid': SimpleAvoidAlgorithm,
    'quadrant': QuadrantAvoidAlgorithm,
}


class SimpleBot:
    def __init__(self, algorithm: GameAlgorithm, username: str):
        self.username = username
        self.client = GameClient(username, password="your_password")
        self.game_state = GameState()
        self.algorithm = algorithm
        self.play()

    def play(self):
        if self.client.connect():
            print(f'Connected! Using {self.algorithm.__class__.__name__}')

            while True:
                messages = self.client.get_messages()

                for msg in messages:
                    print(f">> {msg}")
                    self.handle_message(msg)

                    if msg.startswith('tick'):
                        move = self.algorithm.get_move(self.game_state)
                        self.client.socket.send(f'move|{move}\n'.encode())
                        print(f"Map: {self.game_state.map_size}, Pos: {self.game_state.my_position} -> {move}")

                time.sleep(0.01)
        else:
            print("Failed to connect!")

    def handle_message(self, msg):
        parts = msg.split("|")
        if len(parts) > 1:
            command = parts[0]
            if command == "game":
                self.handle_game(parts)
            elif command == "limit":
                self.handle_limit(parts)
            elif command == "player":
                self.handle_player(parts)
            elif command == "pos":
                self.handle_position(parts)
            elif command == "die":
                self.handle_death(parts)
            elif command == "gameover":
                print("Game Over!")
                exit(0)

    def handle_game(self, msg):
        width = int(msg[1])
        height = int(msg[2])
        my_player_id = int(msg[3])
        self.game_state.start_game(width, height, my_player_id)

    def handle_limit(self, msg):
        width = int(msg[3]) + 1
        height = int(msg[4]) + 1
        self.game_state.set_map_size(width, height)

    def handle_player(self, msg):
        player_id = int(msg[1])
        player_username = msg[2]
        self.game_state.add_player(player_id, player_username)

    def handle_position(self, msg):
        player_id = int(msg[1])
        x = int(msg[2])
        y = int(msg[3])
        self.game_state.add_player_position(player_id, x, y)

    def handle_death(self, msg):
        player_id = int(msg[1])
        self.game_state.kill_player(player_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GPN Tron Bot')
    parser.add_argument(
        '-a', '--algorithm',
        choices=ALGORITHMS.keys(),
        default='avoid',
        help='Algorithm to use (default: avoid)'
    )
    args = parser.parse_args()

    algo_name = args.algorithm
    algorithm = ALGORITHMS[algo_name]()
    bot = SimpleBot(algorithm, username=algo_name)
