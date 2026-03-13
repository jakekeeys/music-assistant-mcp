"""Entry points for the Music Assistant MCP Server.

Provides ``main()`` (stdio) and ``main_web()`` (HTTP) transport modes.
"""

from __future__ import annotations

import asyncio
import logging
import signal
import sys

from music_assistant_mcp.server import create_server

logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )


async def _run_stdio() -> None:
    """Run the MCP server over stdio (for Claude Desktop, etc.)."""
    mcp, client = create_server()
    try:
        await mcp.run_async(transport="stdio")
    finally:
        await client.close()


async def _run_web() -> None:
    """Run the MCP server over HTTP (streamable HTTP transport)."""
    from music_assistant_mcp.config import settings

    mcp, client = create_server()
    try:
        await mcp.run_async(
            transport="streamable-http",
            host=settings.host,
            port=settings.port,
        )
    finally:
        await client.close()


def _handle_signals() -> None:
    """Register graceful shutdown on SIGTERM/SIGINT."""
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, lambda: loop.stop())
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            pass


def main() -> None:
    """stdio transport entry point (default for Claude Desktop / Claude Code)."""
    _setup_logging()
    logger.info("Starting Music Assistant MCP Server (stdio)")
    asyncio.run(_run_stdio())


def main_web() -> None:
    """HTTP transport entry point."""
    _setup_logging()
    from music_assistant_mcp.config import settings

    logger.info(
        "Starting Music Assistant MCP Server (HTTP) on %s:%s",
        settings.host,
        settings.port,
    )
    asyncio.run(_run_web())


if __name__ == "__main__":
    main()
