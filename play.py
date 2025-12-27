import time
from connect import GameClient

username = "your_username"
password = "your_password"

class SimpleBot:
    def __init__(self):
        self.client = GameClient(username, password)
        self.play()

    def play(self):
        if self.client.connect():
            print('🚀 Connected and logged in!')
            
            while True:
                messages = self.client.get_messages()
                
                for msg in messages:
                    print(f"📩 {msg}")
                    
                    # When server says it's time to move, always go up
                    if msg.startswith('tick'):
                        self.client.socket.send(b'move|up\n')
                        print("⬆️  Moved up!")
                
                time.sleep(0.01)
        else:
            print("❌ Failed to connect!")

if __name__ == "__main__":
    bot = SimpleBot()

    