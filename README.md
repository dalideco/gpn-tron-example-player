# GPN Tron example player

A simple Python bot for playing the GPN Tron game.

## About

This project contains a bot that connects to a Tron game server and plays automatically. The bot uses the `GameClient` class to handle communication with the game server.

## Links

- **View Server (watch games live)**: https://tron.thekurisu.org/
- **Game Server Repository**: https://github.com/Kurisudes/gpn-tron
- **Protocol Documentation**: https://github.com/Kurisudes/gpn-tron/blob/master/PROTOCOL.md

## Quick Start

1. Install dependencies:
   ```bash
   pip install dnspython
   ```

2. Run the simple example bot:
   ```bash
   python3 play.py
   ```

## Files

- `connect.py` - GameClient class for connecting to the server
- `play.py` - Simple example bot that always moves up
