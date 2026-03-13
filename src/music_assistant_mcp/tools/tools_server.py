"""Server information and utility tools."""

from __future__ import annotations

from typing import Any


def register_server_tools(mcp: Any, client: Any) -> None:
    """Register server info and utility tools."""

    @mcp.tool()
    async def ma_get_server_info() -> dict[str, Any]:
        """Get Music Assistant server information.

        Returns server version, server ID, and basic status information.
        Use this as a health check or to verify connectivity.

        Returns:
            Server info dict with server_id, server_version, schema_version,
            and other metadata.
        """
        return await client.get_server_info()

    @mcp.tool()
    async def ma_run_command(
        command: str,
        args: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute any Music Assistant API command directly.

        This is an escape-hatch for commands not covered by other tools.
        Refer to the Music Assistant API docs at /api-docs for all available
        commands.

        Args:
            command: The command path (e.g. "music/sync", "config/providers/get").
            args: Optional dict of arguments for the command.

        Returns:
            The raw API response.

        Examples:
            - Sync music library: ma_run_command("music/sync")
            - Get provider config: ma_run_command("config/providers/get",
                args={"instance_id": "spotify--1234"})
        """
        kwargs = args or {}
        result = await client.command(command, **kwargs)
        return {"command": command, "result": result}
