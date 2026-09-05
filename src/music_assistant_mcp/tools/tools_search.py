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
        library_only: bool = False,
        providers: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search across all music providers for tracks, albums, artists, playlists, and radio stations.

        Args:
            query: Search query string (e.g. "Bohemian Rhapsody", "Miles Davis").
            media_types: Optional list to restrict search. Values: "track", "album",
                "artist", "playlist", "radio". Default: search all types.
            limit: Maximum results per media type (default 10, max 100).
            library_only: Only search the local library, not online providers.
            providers: Restrict to these provider instance ids or domains.

        Returns:
            Results grouped by media type, each with name, URI, provider info.

        Examples:
            - Search for a song: ma_search("Bohemian Rhapsody")
            - Search only albums: ma_search("Kind of Blue", media_types=["album"])
            - Search artists: ma_search("Taylor Swift", media_types=["artist"])
        """
        return await client.search(
            query,
            media_types=media_types,
            limit=limit,
            library_only=library_only,
            providers=providers,
        )

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
        """Get tracks by a specific artist.

        For a library artist this returns the in-library tracks. Use
        ma_run_command("music/artists/top_tracks", ...) for provider top tracks.

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

    @mcp.tool()
    async def ma_get_item_by_name(
        name: str,
        artist: str | None = None,
        album: str | None = None,
        media_type: str | None = None,
    ) -> dict[str, Any]:
        """Find a single media item by name, e.g. a playlist or album the user named.

        Faster than ma_search when you already know what you're looking for.

        Args:
            name: Item name (e.g. "Road Trip", "Kind of Blue").
            artist: Optional artist name to disambiguate.
            album: Optional album name to disambiguate.
            media_type: Optional type: "track", "album", "artist", "playlist", "radio".

        Returns:
            The best-matching item, or null.
        """
        return await client.command(
            "music/item_by_name", name=name, artist=artist, album=album, media_type=media_type
        )

    @mcp.tool()
    async def ma_get_track_by_name(
        track_name: str,
        artist_name: str | None = None,
        album_name: str | None = None,
    ) -> dict[str, Any]:
        """Find a single track by name and optional artist/album.

        Args:
            track_name: Track title.
            artist_name: Optional artist name.
            album_name: Optional album name.

        Returns:
            The best-matching track, or null.
        """
        return await client.command(
            "music/track_by_name",
            track_name=track_name,
            artist_name=artist_name,
            album_name=album_name,
        )

    @mcp.tool()
    async def ma_get_artist_top_tracks(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        """Get the top / most popular tracks for an artist across providers.

        Args:
            item_id: The artist ID.
            provider_instance_id_or_domain: Provider to query (default "library").
        """
        items = await client.command(
            "music/artists/top_tracks",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )
        return {"tracks": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_similar_artists(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
        limit: int = 25,
    ) -> dict[str, Any]:
        """Get artists similar to the given artist.

        Args:
            item_id: The artist ID.
            provider_instance_id_or_domain: Provider to query (default "library").
            limit: Max results (default 25).
        """
        items = await client.command(
            "music/artists/similar_artists",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
            limit=limit,
        )
        return {"artists": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_similar_tracks(
        item_id: str,
        provider_instance_id_or_domain: str = "library",
        limit: int = 25,
    ) -> dict[str, Any]:
        """Get tracks similar to the given track ("more like this").

        Args:
            item_id: The track ID.
            provider_instance_id_or_domain: Provider to query (default "library").
            limit: Max results (default 25).
        """
        items = await client.command(
            "music/tracks/similar_tracks",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
            limit=limit,
        )
        return {"tracks": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_recommendations() -> dict[str, Any]:
        """Get recommendation rows (e.g. "Recently played", "Discover", provider picks).

        Rows come without their items. Pass a row's provider and item_id to
        ma_get_recommendation_items to fetch them.
        """
        rows = await client.command("music/recommendations")
        return {"rows": rows, "count": len(rows)}

    @mcp.tool()
    async def ma_get_recommendation_items(provider: str, item_id: str) -> dict[str, Any]:
        """Get the items for one recommendation row from ma_get_recommendations.

        Args:
            provider: The row's provider.
            item_id: The row's item_id.
        """
        items = await client.command(
            "music/recommendations/items", provider=provider, item_id=item_id
        )
        return {"items": items, "count": len(items)}

    @mcp.tool()
    async def ma_get_library_genres(
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List genres in the library, optionally filtered by name.

        Args:
            search: Optional name filter (e.g. "jazz").
            limit: Max items (default 50).
            offset: Pagination offset.
        """
        items = await client.command(
            "music/genres/library_items", search=search, limit=limit, offset=offset
        )
        return {"genres": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_genre_tracks(
        item_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        """Get library tracks mapped to a genre.

        Args:
            item_id: The genre ID (from ma_get_library_genres).
            limit: Max items (default 50).
            offset: Pagination offset.
        """
        items = await client.command(
            "music/genres/tracks", item_id=item_id, limit=limit, offset=offset
        )
        return {"tracks": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_genre_albums(
        item_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        """Get library albums mapped to a genre.

        Args:
            item_id: The genre ID (from ma_get_library_genres).
            limit: Max items (default 50).
            offset: Pagination offset.
        """
        items = await client.command(
            "music/genres/albums", item_id=item_id, limit=limit, offset=offset
        )
        return {"albums": items, "count": len(items), "offset": offset, "limit": limit}

    @mcp.tool()
    async def ma_get_track_lyrics(track_uri: str) -> dict[str, Any]:
        """Get lyrics for a track.

        Args:
            track_uri: The track URI (e.g. "library://track/42").

        Returns:
            Plain lyrics and, if available, time-synced LRC lyrics.
        """
        track = await client.get_item_by_uri(track_uri)
        lyrics, lrc = await client.command("metadata/get_track_lyrics", track=track)
        return {"uri": track_uri, "lyrics": lyrics, "lrc_lyrics": lrc}
