"""HTTP API client for the Music Assistant server.

Communicates via POST /api using the JSON-RPC style command format that
Music Assistant exposes. This is the same protocol the WebSocket uses,
but over plain HTTP for stateless request/response.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_TIMEOUT = 30.0


class MusicAssistantClient:
    """Async HTTP client for the Music Assistant server API."""

    def __init__(self, base_url: str, token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._message_id = 0
        self._http: httpx.AsyncClient | None = None

    # -- lifecycle -----------------------------------------------------------

    async def _get_http(self) -> httpx.AsyncClient:
        if self._http is None or self._http.is_closed:
            self._http = httpx.AsyncClient(
                base_url=self._base_url,
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "Content-Type": "application/json",
                },
                timeout=_TIMEOUT,
            )
        return self._http

    async def close(self) -> None:
        if self._http and not self._http.is_closed:
            await self._http.aclose()

    # -- low-level command ---------------------------------------------------

    async def command(self, command: str, **kwargs: Any) -> Any:
        """Send a command to Music Assistant and return the result.

        Args:
            command: The API command path, e.g. ``"players/all"`` or
                ``"music/search"``.
            **kwargs: Arguments forwarded as the ``args`` dict in the
                JSON-RPC payload.

        Returns:
            The ``result`` field from the response, or the full response
            dict if no ``result`` key is present.

        Raises:
            MusicAssistantError: If the server returns an error.
            httpx.HTTPStatusError: On HTTP-level failures.
        """
        self._message_id += 1
        payload: dict[str, Any] = {
            "message_id": str(self._message_id),
            "command": command,
        }
        # Only include args if we actually have some
        args = {k: v for k, v in kwargs.items() if v is not None}
        if args:
            payload["args"] = args

        http = await self._get_http()
        logger.debug("→ %s %s", command, json.dumps(args) if args else "")
        resp = await http.post("/api", json=payload)
        resp.raise_for_status()

        data = resp.json()
        # The MA API returns errors as {"error": {"message": ..., "code": ...}}
        # and results directly as the top-level JSON (list or dict).
        if isinstance(data, dict) and "error" in data:
            err = data["error"]
            if isinstance(err, dict):
                raise MusicAssistantError(
                    err.get("message", str(err)),
                    err.get("code"),
                )
            raise MusicAssistantError(str(err))
        return data

    # -- convenience helpers -------------------------------------------------

    async def get_server_info(self) -> dict[str, Any]:
        """Get basic server information (no auth required for /info)."""
        http = await self._get_http()
        resp = await http.get("/info")
        resp.raise_for_status()
        return resp.json()

    # -- players -------------------------------------------------------------

    async def get_players(self) -> list[dict[str, Any]]:
        return await self.command("players/all")

    async def get_player(self, player_id: str) -> dict[str, Any]:
        return await self.command("players/get", player_id=player_id)

    async def player_command(
        self, player_id: str, cmd: str, **kwargs: Any
    ) -> Any:
        return await self.command(f"players/cmd/{cmd}", player_id=player_id, **kwargs)

    # -- player queues -------------------------------------------------------

    async def get_queues(self) -> list[dict[str, Any]]:
        return await self.command("player_queues/all")

    async def get_queue_items(
        self, queue_id: str, limit: int = 25, offset: int = 0
    ) -> list[dict[str, Any]]:
        return await self.command(
            "player_queues/items", queue_id=queue_id, limit=limit, offset=offset
        )

    async def queue_command(self, queue_id: str, cmd: str, **kwargs: Any) -> Any:
        return await self.command(f"player_queues/{cmd}", queue_id=queue_id, **kwargs)

    # -- music library -------------------------------------------------------

    async def search(
        self,
        search_query: str,
        media_types: list[str] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        return await self.command(
            "music/search",
            search_query=search_query,
            media_types=media_types,
            limit=limit,
        )

    async def get_library_items(
        self,
        media_type: str,
        limit: int = 25,
        offset: int = 0,
        order_by: str | None = None,
        in_library_only: bool = True,
    ) -> list[dict[str, Any]]:
        return await self.command(
            f"music/{media_type}s/library_items",
            limit=limit,
            offset=offset,
            order_by=order_by,
            in_library_only=in_library_only,
        )

    async def get_item(
        self,
        media_type: str,
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> dict[str, Any]:
        return await self.command(
            f"music/{media_type}s/get",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )

    async def get_item_by_uri(self, uri: str) -> dict[str, Any]:
        return await self.command("music/item_by_uri", uri=uri)

    async def get_artist_albums(
        self,
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> list[dict[str, Any]]:
        return await self.command(
            "music/artists/artist_albums",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )

    async def get_artist_tracks(
        self,
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> list[dict[str, Any]]:
        return await self.command(
            "music/artists/artist_tracks",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )

    async def get_album_tracks(
        self,
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> list[dict[str, Any]]:
        return await self.command(
            "music/albums/album_tracks",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )

    async def get_playlist_tracks(
        self,
        item_id: str,
        provider_instance_id_or_domain: str = "library",
    ) -> list[dict[str, Any]]:
        return await self.command(
            "music/playlists/playlist_tracks",
            item_id=item_id,
            provider_instance_id_or_domain=provider_instance_id_or_domain,
        )

    # -- playlist management -------------------------------------------------

    async def create_playlist(self, name: str) -> dict[str, Any]:
        return await self.command("music/playlists/create", name=name)

    async def add_playlist_tracks(
        self, db_playlist_id: str, uris: list[str]
    ) -> None:
        await self.command(
            "music/playlists/add_playlist_tracks",
            db_playlist_id=db_playlist_id,
            uris=uris,
        )

    async def remove_playlist_tracks(
        self, db_playlist_id: str, positions: list[int]
    ) -> None:
        await self.command(
            "music/playlists/remove_playlist_tracks",
            db_playlist_id=db_playlist_id,
            positions_to_remove=positions,
        )

    # -- favorites -----------------------------------------------------------

    async def add_to_favorites(self, item_uri: str) -> None:
        await self.command("music/favorites/add_item", item=item_uri)

    async def remove_from_favorites(self, item_uri: str) -> None:
        await self.command("music/favorites/remove_item", item=item_uri)

    # -- recently played / in-progress ---------------------------------------

    async def get_recently_played(self, limit: int = 10) -> list[dict[str, Any]]:
        return await self.command("music/recently_played_items", limit=limit)


class MusicAssistantError(Exception):
    """Error returned by the Music Assistant API."""

    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code
