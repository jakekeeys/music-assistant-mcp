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
    async def ma_player_play_announcement(
        player_id: str,
        url: str | None = None,
        message: str | None = None,
        volume_level: int | None = None,
    ) -> dict[str, Any]:
        """Play an announcement (audio URL or TTS message) on a player.

        The current playback is paused, the announcement plays, and then
        playback resumes automatically. Provide either url or message.

        Args:
            player_id: The player to play the announcement on.
            url: URL of the audio to play as announcement.
            message: Text to speak via the server's TTS engine.
            volume_level: Optional volume level for the announcement (0-100).
                Current volume is restored after.

        Returns:
            Success status.
        """
        await client.player_command(
            player_id,
            "play_announcement",
            url=url,
            message=message,
            volume_level=volume_level,
        )
        return {"success": True, "player_id": player_id, "url": url, "message": message}

    @mcp.tool()
    async def ma_get_player_by_name(name: str) -> dict[str, Any]:
        """Look up a player by its display name (e.g. "Living Room").

        Args:
            name: The player name as shown in Music Assistant.

        Returns:
            Player details, or null if no player matches.
        """
        return await client.command("players/get_by_name", name=name)

    @mcp.tool()
    async def ma_player_power(player_id: str, powered: bool) -> dict[str, Any]:
        """Power a player on or off.

        Args:
            player_id: The player to control.
            powered: True to power on, False to power off.
        """
        await client.player_command(player_id, "power", powered=powered)
        return {"success": True, "player_id": player_id, "powered": powered}

    @mcp.tool()
    async def ma_player_group(player_id: str, target_player: str) -> dict[str, Any]:
        """Join a player to another player so they play in sync (multi-room).

        Args:
            player_id: The player to add to the group.
            target_player: The player to join (becomes/stays the group leader).
        """
        await client.player_command(player_id, "group", target_player=target_player)
        return {"success": True, "player_id": player_id, "joined": target_player}

    @mcp.tool()
    async def ma_player_ungroup(player_id: str) -> dict[str, Any]:
        """Remove a player from its sync group so it plays on its own again.

        Args:
            player_id: The player to detach.
        """
        await client.player_command(player_id, "ungroup")
        return {"success": True, "player_id": player_id, "action": "ungroup"}

    @mcp.tool()
    async def ma_player_set_group_members(
        target_player: str,
        player_ids_to_add: list[str] | None = None,
        player_ids_to_remove: list[str] | None = None,
    ) -> dict[str, Any]:
        """Add and/or remove several players to/from a group in one call.

        Args:
            target_player: The group leader player.
            player_ids_to_add: Players to join to the leader.
            player_ids_to_remove: Players to detach from the leader.
        """
        await client.command(
            "players/cmd/set_members",
            target_player=target_player,
            player_ids_to_add=player_ids_to_add,
            player_ids_to_remove=player_ids_to_remove,
        )
        return {
            "success": True,
            "target_player": target_player,
            "added": player_ids_to_add or [],
            "removed": player_ids_to_remove or [],
        }

    @mcp.tool()
    async def ma_player_group_volume_set(
        player_id: str, volume_level: int
    ) -> dict[str, Any]:
        """Set the overall volume of a player group (all synced members).

        Args:
            player_id: The group leader (or any grouped player).
            volume_level: Volume level 0-100 applied across the group.
        """
        await client.player_command(player_id, "group_volume", volume_level=volume_level)
        return {"success": True, "player_id": player_id, "volume_level": volume_level}

    @mcp.tool()
    async def ma_player_sleep_timer_set(player_id: str, seconds: int) -> dict[str, Any]:
        """Stop playback on a player after a delay ("turn off in 30 minutes").

        Args:
            player_id: The player to schedule.
            seconds: Delay until playback stops.

        Returns:
            The expiry as a UTC unix timestamp.
        """
        expires = await client.command(
            "players/sleep_timer/set", player_id=player_id, seconds=seconds
        )
        return {"success": True, "player_id": player_id, "expires_at": expires}

    @mcp.tool()
    async def ma_player_sleep_timer_get(player_id: str) -> dict[str, Any]:
        """Get the active sleep timer for a player.

        Args:
            player_id: The player to query.

        Returns:
            Expiry as a UTC unix timestamp, or null if no timer is set.
        """
        expires = await client.command("players/sleep_timer/get", player_id=player_id)
        return {"player_id": player_id, "expires_at": expires}

    @mcp.tool()
    async def ma_player_sleep_timer_clear(player_id: str) -> dict[str, Any]:
        """Cancel the sleep timer on a player.

        Args:
            player_id: The player whose timer to clear.
        """
        await client.command("players/sleep_timer/clear", player_id=player_id)
        return {"success": True, "player_id": player_id, "action": "sleep_timer_clear"}

    @mcp.tool()
    async def ma_player_add_current_to_favorites(player_id: str) -> dict[str, Any]:
        """Favorite whatever is currently playing on a player ("like this song").

        Args:
            player_id: The player that is playing the item.
        """
        await client.command("players/add_currently_playing_to_favorites", player_id=player_id)
        return {"success": True, "player_id": player_id, "action": "added_current_to_favorites"}
