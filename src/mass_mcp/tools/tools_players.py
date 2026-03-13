"""Player control tools."""

from __future__ import annotations

from typing import Any


def register_players_tools(mcp: Any, client: Any) -> None:
    """Register player control tools."""

    @mcp.tool()
    async def ma_get_players() -> dict[str, Any]:
        """List all available players (speakers/devices).

        Returns a list of all players registered in Music Assistant, including
        their current state (playing, paused, idle), volume level, name, and
        capabilities.

        Returns:
            List of player objects with player_id, name, state, volume_level,
            type, and available features.
        """
        players = await client.get_players()
        return {"players": players, "count": len(players)}

    @mcp.tool()
    async def ma_get_player(player_id: str) -> dict[str, Any]:
        """Get detailed information about a specific player.

        Args:
            player_id: The unique player identifier.

        Returns:
            Full player details including state, volume, current media,
            capabilities, and group membership.
        """
        return await client.get_player(player_id)

    @mcp.tool()
    async def ma_player_play(player_id: str) -> dict[str, Any]:
        """Start or resume playback on a player.

        Args:
            player_id: The player to start playing on.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "play")
        return {"success": True, "player_id": player_id, "action": "play"}

    @mcp.tool()
    async def ma_player_pause(player_id: str) -> dict[str, Any]:
        """Pause playback on a player.

        Args:
            player_id: The player to pause.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "pause")
        return {"success": True, "player_id": player_id, "action": "pause"}

    @mcp.tool()
    async def ma_player_stop(player_id: str) -> dict[str, Any]:
        """Stop playback on a player and clear the current item.

        Args:
            player_id: The player to stop.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "stop")
        return {"success": True, "player_id": player_id, "action": "stop"}

    @mcp.tool()
    async def ma_player_play_pause(player_id: str) -> dict[str, Any]:
        """Toggle play/pause on a player.

        Args:
            player_id: The player to toggle.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "play_pause")
        return {"success": True, "player_id": player_id, "action": "play_pause"}

    @mcp.tool()
    async def ma_player_volume_set(
        player_id: str, volume_level: int
    ) -> dict[str, Any]:
        """Set the volume level on a player.

        Args:
            player_id: The player to adjust.
            volume_level: Volume level from 0 (mute) to 100 (max).

        Returns:
            Success status with the new volume level.
        """
        await client.player_command(
            player_id, "volume_set", volume_level=volume_level
        )
        return {
            "success": True,
            "player_id": player_id,
            "volume_level": volume_level,
        }

    @mcp.tool()
    async def ma_player_volume_up(player_id: str) -> dict[str, Any]:
        """Increase the volume on a player by one step.

        Args:
            player_id: The player to adjust.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "volume_up")
        return {"success": True, "player_id": player_id, "action": "volume_up"}

    @mcp.tool()
    async def ma_player_volume_down(player_id: str) -> dict[str, Any]:
        """Decrease the volume on a player by one step.

        Args:
            player_id: The player to adjust.

        Returns:
            Success status.
        """
        await client.player_command(player_id, "volume_down")
        return {"success": True, "player_id": player_id, "action": "volume_down"}

    @mcp.tool()
    async def ma_player_volume_mute(
        player_id: str, muted: bool = True
    ) -> dict[str, Any]:
        """Mute or unmute a player.

        Args:
            player_id: The player to mute/unmute.
            muted: True to mute, False to unmute (default True).

        Returns:
            Success status.
        """
        await client.player_command(player_id, "volume_mute", muted=muted)
        return {
            "success": True,
            "player_id": player_id,
            "muted": muted,
        }

    @mcp.tool()
    async def ma_player_play_media(
        player_id: str,
        media: str,
    ) -> dict[str, Any]:
        """Play a specific media item on a player directly (bypasses queue).

        Args:
            player_id: The player to play on.
            media: Media URI or URL to play (e.g. "spotify://track/1234",
                "http://example.com/stream.mp3").

        Returns:
            Success status.
        """
        await client.player_command(player_id, "play_media", media=media)
        return {"success": True, "player_id": player_id, "media": media}

    @mcp.tool()
    async def ma_player_play_announcement(
        player_id: str,
        url: str,
        volume_level: int | None = None,
    ) -> dict[str, Any]:
        """Play an announcement (TTS or audio URL) on a player.

        The current playback is paused, the announcement plays, and then
        playback resumes automatically.

        Args:
            player_id: The player to play the announcement on.
            url: URL of the audio to play as announcement.
            volume_level: Optional volume level for the announcement (0-100).
                Current volume is restored after.

        Returns:
            Success status.
        """
        kwargs: dict[str, Any] = {"url": url}
        if volume_level is not None:
            kwargs["volume_level"] = volume_level
        await client.player_command(player_id, "play_announcement", **kwargs)
        return {"success": True, "player_id": player_id, "url": url}
