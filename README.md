# Music Assistant MCP Server

An MCP (Model Context Protocol) server that enables AI assistants to interact with [Music Assistant](https://music-assistant.io). Control your music library, players, queues, and playlists using natural language.

Built with [FastMCP](https://github.com/jlowin/fastmcp).

## Features

| Category | Tools | Description |
|----------|-------|-------------|
| **Search & Browse** | 15 tools | Search all providers, browse artists/albums/tracks/playlists/radio, get details |
| **Player Control** | 11 tools | Play, pause, stop, volume, mute, play media, announcements |
| **Queue Management** | 11 tools | Play media on queue, next/prev, shuffle, repeat, clear, transfer between players |
| **Playlists** | 3 tools | Create playlists, add/remove tracks |
| **Favorites** | 2 tools | Add/remove items from library favorites |
| **Server** | 2 tools | Server info, raw command escape-hatch |
| **Total** | **46 tools** | |

## Quick Start

### Prerequisites

- Python 3.12+
- A running [Music Assistant](https://music-assistant.io/installation/) server
- A long-lived access token from Music Assistant

### Get a Token

1. Open your Music Assistant UI (default: `http://localhost:8095`)
2. Go to **Settings > Users**
3. Create a new token (long-lived recommended for integrations)

### Install

```bash
pip install -e .
```

### Configure

Set environment variables (or create a `.env` file):

```bash
export MASS_URL=http://localhost:8095
export MASS_TOKEN=your_token_here
```

### Run

**stdio mode** (for Claude Desktop, Claude Code, etc.):
```bash
music-assistant-mcp
```

**HTTP mode** (for web clients):
```bash
music-assistant-mcp-web
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "music-assistant": {
      "command": "music-assistant-mcp",
      "env": {
        "MASS_URL": "http://localhost:8095",
        "MASS_TOKEN": "your_token_here"
      }
    }
  }
}
```

Or using uvx (no install needed):

```json
{
  "mcpServers": {
    "music-assistant": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/jakekeeys/music-assistant-mcp", "music-assistant-mcp"],
      "env": {
        "MASS_URL": "http://localhost:8095",
        "MASS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Example Conversations

| You Say | What Happens |
|---------|-------------|
| *"What's playing right now?"* | Checks player states and current queue items |
| *"Play some Miles Davis in the living room"* | Searches for Miles Davis, plays on the living room speaker |
| *"Turn the volume down to 30% on the kitchen speaker"* | Sets volume on the specified player |
| *"Add this song to my Road Trip playlist"* | Adds the current track to the named playlist |
| *"Skip to the next track"* | Advances the queue |
| *"Shuffle the queue and turn on repeat"* | Configures queue settings |
| *"Transfer the music to the bedroom speaker"* | Moves the queue between players seamlessly |
| *"What albums do I have by Radiohead?"* | Searches the library for the artist's albums |

## Architecture

```
src/music_assistant_mcp/
├── __init__.py          # Package version
├── __main__.py          # Entry points (stdio, HTTP)
├── config.py            # Settings from env vars
├── server.py            # FastMCP server + auto-discovery
├── client/
│   └── api_client.py    # HTTP client for MA's POST /api
└── tools/
    ├── tools_search.py    # Library browsing & search (15 tools)
    ├── tools_players.py   # Player control (11 tools)
    ├── tools_queues.py    # Queue management (11 tools)
    ├── tools_playlists.py # Playlist CRUD (3 tools)
    ├── tools_favorites.py # Favorites (2 tools)
    └── tools_server.py    # Server info & raw commands (2 tools)
```

### Adding New Tools

1. Create `src/music_assistant_mcp/tools/tools_<category>.py`
2. Define `register_<category>_tools(mcp, client)` 
3. Use `@mcp.tool()` to register tools
4. They're auto-discovered on startup

## How It Works

The server communicates with Music Assistant via its HTTP JSON-RPC API (`POST /api`). This is the same protocol the WebSocket interface uses, but stateless. Every command is sent as:

```json
{
  "message_id": "1",
  "command": "players/cmd/play",
  "args": { "player_id": "living_room" }
}
```

Authentication is via a Bearer token in the `Authorization` header.

## License

MIT
