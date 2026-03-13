"""Playlist management tools."""

from __future__ import annotations

from typing import Any


def register_playlists_tools(mcp: Any, client: Any) -> None:
    """Register playlist management tools."""

    @mcp.tool()
    async def ma_create_playlist(name: str) -> dict[str, Any]:
        """Create a new playlist.

        Args:
            name: Name for the new playlist.

        Returns:
            The newly created playlist object with its ID and URI.
        """
        result = await client.create_playlist(name)
        return {"success": True, "playlist": result}

    @mcp.tool()
    async def ma_add_playlist_tracks(
        db_playlist_id: str,
        uris: list[str],
    ) -> dict[str, Any]:
        """Add tracks to an existing playlist.

        Args:
            db_playlist_id: The library playlist ID to add tracks to.
            uris: List of track URIs to add (e.g. ["library://track/1", "spotify://track/abc"]).

        Returns:
            Success status.
        """
        await client.add_playlist_tracks(db_playlist_id, uris)
        return {
            "success": True,
            "playlist_id": db_playlist_id,
            "added_count": len(uris),
        }

    @mcp.tool()
    async def ma_remove_playlist_tracks(
        db_playlist_id: str,
        positions: list[int],
    ) -> dict[str, Any]:
        """Remove tracks from a playlist by their position.

        Args:
            db_playlist_id: The library playlist ID.
            positions: List of zero-based positions to remove.

        Returns:
            Success status.
        """
        await client.remove_playlist_tracks(db_playlist_id, positions)
        return {
            "success": True,
            "playlist_id": db_playlist_id,
            "removed_positions": positions,
        }
