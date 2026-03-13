"""Search and library browsing tools."""

from __future__ import annotations

from typing import Any


def register_search_tools(mcp: Any, client: Any) -> None:
    """Register music search and library browsing tools."""

    @mcp.tool()
    async def ma_search(
        query: str,
        media_types: list[str] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search across all music providers for tracks, albums, artists, playlists, and radio stations.

        Args:
            query: Search query string (e.g. "Bohemian Rhapsody", "Miles Davis").
            media_types: Optional list to restrict search. Values: "track", "album",
                "artist", "playlist", "radio". Default: search all types.
            limit: Maximum results per media type (default 10, max 100).

        Returns:
            Results grouped by media type, each with name, URI, provider info.

        Examples:
            - Search for a song: ma_search("Bohemian Rhapsody")
            - Search only albums: ma_search("Kind of Blue", media_types=["album"])
            - Search artists: ma_search("Taylor Swift", media_types=["artist"])
        """
        return await client.search(query, media_types=media_types, limit=limit)

    @mcp.tool()
    async def ma_get_library_artists(
        limit: int = 25,
        offset: int = 0,
        order_by: str | None = None,
    ) -> dict[str, Any]:
        """List artists in the music library.

        Args:
            limit: Max items to return (default 25).
            offset: Pagination offset.
            order_by: Sort field (e.g. "name", "sort_name", "timestamp_added").

        Returns:
            List of artist objects with name, URI, image, and provider info.
        """
        items = await client.get_library_items(
            "artist", limit=limit, offset=offset, order_by=order_by
        )
        return {"artists": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_library_albums(
        limit: int = 25,
        offset: int = 0,
        order_by: str | None = None,
    ) -> dict[str, Any]:
        """List albums in the music library.

        Args:
            limit: Max items to return (default 25).
            offset: Pagination offset.
            order_by: Sort field (e.g. "name", "sort_name", "year", "timestamp_added").

        Returns:
            List of album objects with name, artist, year, URI, and provider info.
        """
        items = await client.get_library_items(
            "album", limit=limit, offset=offset, order_by=order_by
        )
        return {"albums": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_library_tracks(
        limit: int = 25,
        offset: int = 0,
        order_by: str | None = None,
    ) -> dict[str, Any]:
        """List tracks in the music library.

        Args:
            limit: Max items to return (default 25).
            offset: Pagination offset.
            order_by: Sort field (e.g. "name", "sort_name", "timestamp_added").

        Returns:
            List of track objects with name, artist, album, duration, URI.
        """
        items = await client.get_library_items(
            "track", limit=limit, offset=offset, order_by=order_by
        )
        return {"tracks": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_library_playlists(
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List playlists in the music library.

        Args:
            limit: Max items to return (default 25).
            offset: Pagination offset.

        Returns:
            List of playlist objects with name, owner, URI, and provider info.
        """
        items = await client.get_library_items(
            "playlist", limit=limit, offset=offset
        )
        return {"playlists": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_library_radio_stations(
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List radio stations in the music library.

        Args:
            limit: Max items to return (default 25).
            offset: Pagination offset.

        Returns:
            List of radio station objects with name, URI, and provider info.
        """
        items = await client.get_library_items(
            "radio", limit=limit, offset=offset
        )
        return {"radio_stations": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_artist(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get detailed information about a specific artist.

        Args:
            item_id: The artist ID (numeric or string).
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            Full artist details including name, image, biography, and provider info.
        """
        return await client.get_item("artist", item_id, provider_instance_id_or_domain)

    @mcp.tool()
    async def ma_get_album(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get detailed information about a specific album.

        Args:
            item_id: The album ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            Full album details including name, artist, year, tracks, and provider info.
        """
        return await client.get_item("album", item_id, provider_instance_id_or_domain)

    @mcp.tool()
    async def ma_get_track(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get detailed information about a specific track.

        Args:
            item_id: The track ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            Full track details including name, artist, album, duration, and provider info.
        """
        return await client.get_item("track", item_id, provider_instance_id_or_domain)

    @mcp.tool()
    async def ma_get_artist_albums(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get all albums by a specific artist.

        Args:
            item_id: The artist ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            List of albums by the artist.
        """
        items = await client.get_artist_albums(item_id, provider_instance_id_or_domain)
        return {"albums": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_artist_tracks(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get top tracks by a specific artist.

        Args:
            item_id: The artist ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            List of tracks by the artist.
        """
        items = await client.get_artist_tracks(item_id, provider_instance_id_or_domain)
        return {"tracks": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_album_tracks(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get all tracks on a specific album.

        Args:
            item_id: The album ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            List of tracks on the album, in order.
        """
        items = await client.get_album_tracks(item_id, provider_instance_id_or_domain)
        return {"tracks": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_playlist_tracks(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get all tracks in a specific playlist.

        Args:
            item_id: The playlist ID.
            provider_instance_id_or_domain: Provider to query (default "library").

        Returns:
            List of tracks in the playlist, in order.
        """
        items = await client.get_playlist_tracks(item_id, provider_instance_id_or_domain)
        return {"tracks": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_item_by_uri(uri: str) -> dict[str, Any]:
        """Get full details for any media item by its URI.

        Args:
            uri: The media URI (e.g. "spotify://track/1234", "library://album/5").

        Returns:
            Full item details for the given URI.
        """
        return await client.get_item_by_uri(uri)

    @mcp.tool()
    async def ma_get_recently_played(limit: int = 10) -> dict[str, Any]:
        """Get recently played items.

        Args:
            limit: Maximum number of items to return (default 10).

        Returns:
            List of recently played media items.
        """
        items = await client.get_recently_played(limit=limit)
        return {"items": items, "count": len(items)}
