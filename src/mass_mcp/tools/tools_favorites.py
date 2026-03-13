"""Favorites management tools."""

from __future__ import annotations

from typing import Any


def register_favorites_tools(mcp: Any, client: Any) -> None:
    """Register favorites management tools."""

    @mcp.tool()
    async def ma_add_to_favorites(item_uri: str) -> dict[str, Any]:
        """Add a media item to your favorites / library.

        Works with any media type: tracks, albums, artists, playlists, or
        radio stations.

        Args:
            item_uri: URI of the item to favorite (e.g. "library://track/42",
                "spotify://album/abc").

        Returns:
            Success status.
        """
        await client.add_to_favorites(item_uri)
        return {"success": True, "uri": item_uri, "action": "added_to_favorites"}

    @mcp.tool()
    async def ma_remove_from_favorites(item_uri: str) -> dict[str, Any]:
        """Remove a media item from your favorites / library.

        Args:
            item_uri: URI of the item to un-favorite.

        Returns:
            Success status.
        """
        await client.remove_from_favorites(item_uri)
        return {"success": True, "uri": item_uri, "action": "removed_from_favorites"}
