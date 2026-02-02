import socket
import time
import dns.resolver

class GameClient:
    def __init__(self, user, password):
        self.domain = "localhost"
        self.port = 4000
        self.user = user
        self.password = password
        self.socket = None
        self.buffer = ""  # Internal storage for incomplete TCP packets

    def _resolve_srv(self):
        """Internal method: Resolves host:port via SRV record."""
        try:
            print(f"🔍 SRV Lookup for {self.domain}...")
            answers = dns.resolver.resolve(f"_minecraft._tcp.{self.domain}", 'SRV')
            record = answers[0]
            # rstrip removes trailing dot from DNS response
            return str(record.target).rstrip('.'), record.port
        except Exception as e:
            print(f"⚠️ DNS Fallback: {e}")
            return self.domain, 25565

    def connect(self):
        """Connects, waits for greeting, and performs login."""
        # Close old socket if it exists
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

        host, port = self.domain, self.port

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((host, port))
            print(f"✅ Socket connected to {host}:{port}")

            # 1. Wait for server greeting ("documentation")
            print("⏳ Waiting for handshake...")
            initial_data = self.socket.recv(4096).decode('utf-8')
            
            if "documentation" not in initial_data:
                print(f"❌ Unexpected greeting: {initial_data}")
                return False

            # 2. Send login
            print(f"🔑 Logging in as {self.user}...")
            login_cmd = f"join|{self.user}|{self.password}\n"
            self.socket.sendall(login_cmd.encode('utf-8'))
            return True

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def get_messages(self):
        """
        Reads from socket and returns a LIST of clean messages.
        Handles TCP fragmentation (internal buffer).
        """
        if not self.socket:
            return []

        try:
            # Attempt to read data
            data = self.socket.recv(4096).decode('utf-8')
            if not data:
                return [] # Connection closed by server

            # Append data to internal buffer
            self.buffer += data

            # If we have a newline, we can extract complete messages
            if '\n' in self.buffer:
                # Split at newline
                parts = self.buffer.split('\n')
                
                # The last part is either empty (if data ended with \n)
                # or an incomplete new message. Put it back into the buffer.
                self.buffer = parts.pop()
                
                # Return all complete parts
                return parts
            
            return []

        except socket.timeout:
            return [] # Nothing to read is okay
        except Exception as e:
            print(f"⚠️ Read error: {e}")
            return []
