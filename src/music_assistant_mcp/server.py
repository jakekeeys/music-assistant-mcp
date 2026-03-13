"""Core MCP server for Music Assistant.

Creates a FastMCP server instance, wires up the API client, and
auto-discovers + registers all tool modules from the ``tools/`` package.
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import Any

from fastmcp import FastMCP

from music_assistant_mcp import __version__
from music_assistant_mcp.client.api_client import MusicAssistantClient
from music_assistant_mcp.config import settings

logger = logging.getLogger(__name__)


def _discover_tool_modules() -> list[str]:
    """Return dotted module names for every ``tools_*.py`` in the tools package."""
    import music_assistant_mcp.tools as tools_pkg

    modules: list[str] = []
    for info in pkgutil.iter_modules(tools_pkg.__path__):
        if info.name.startswith("tools_"):
            modules.append(f"music_assistant_mcp.tools.{info.name}")
    return modules


def create_server() -> tuple[FastMCP, MusicAssistantClient]:
    """Build and return the configured ``(mcp, client)`` pair.

    All ``tools_*.py`` modules under ``music_assistant_mcp.tools`` are imported and
    their ``register_*_tools(mcp, client)`` function is called automatically.
    """
    mcp = FastMCP(
        name="Music Assistant MCP",
        version=__version__,
    )

    client = MusicAssistantClient(
        base_url=settings.mass_url,
        token=settings.mass_token,
    )

    # Auto-discover and register tools
    for mod_name in sorted(_discover_tool_modules()):
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            logger.exception("Failed to import tool module %s", mod_name)
            continue

        # Convention: each module exposes register_<suffix>_tools(mcp, client)
        short = mod_name.rsplit(".", 1)[-1]  # e.g. "tools_players"
        suffix = short.removeprefix("tools_")  # e.g. "players"
        register_fn_name = f"register_{suffix}_tools"
        register_fn = getattr(mod, register_fn_name, None)
        if register_fn is None:
            logger.warning(
                "Module %s has no %s() function – skipping",
                mod_name,
                register_fn_name,
            )
            continue

        try:
            register_fn(mcp, client)
            logger.debug("Registered tools from %s", mod_name)
        except Exception:
            logger.exception("Error registering tools from %s", mod_name)

    return mcp, client
