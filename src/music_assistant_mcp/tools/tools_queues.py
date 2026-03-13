"""Player queue management tools."""

from __future__ import annotations

from typing import Any


def register_queues_tools(mcp: Any, client: Any) -> None:
    """Register player queue management tools."""

    @mcp.tool()
    async def ma_get_queues() -> dict[str, Any]:
        """List all player queues.

        Each player has an associated queue that holds the list of tracks
        to be played. Returns all queues with their current state.

        Returns:
            List of queue objects with queue_id, current_item, state,
            shuffle/repeat settings, and item count.
        """
        queues = await client.get_queues()
        return {"queues": queues, "count": len(queues)}

    @mcp.tool()
    async def ma_get_queue_items(
        queue_id: str,
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get items in a player queue.

        Args:
            queue_id: The queue identifier (usually same as the player_id).
            limit: Maximum items to return (default 25).
            offset: Pagination offset.

        Returns:
            List of queue items with track details, position, and duration.
        """
        items = await client.get_queue_items(queue_id, limit=limit, offset=offset)
        return {
            "items": items,
            "count": len(items),
            "queue_id": queue_id,
            "offset": offset,
            "limit": limit,
        }

    @mcp.tool()
    async def ma_queue_play_media(
        queue_id: str,
        media: str | list[str],
        option: str = "play",
    ) -> dict[str, Any]:
        """Play media item(s) on a queue.

        This is the primary way to play music. Provide a media URI (from search
        results or library browsing) and it will be queued and played.

        Args:
            queue_id: The queue / player to play on.
            media: Single media URI or list of URIs to play. Examples:
                "spotify://track/1234", "library://album/5",
                "library://playlist/3".
            option: How to add to queue:
                - "play" (default): Clear queue and start playing immediately
                - "replace": Replace queue but don't start playing
                - "next": Insert as next item(s) in queue
                - "replace_next": Replace all upcoming items
                - "add": Add to end of queue

        Returns:
            Success status.

        Examples:
            - Play an album: ma_queue_play_media("player1", "library://album/5")
            - Add to queue: ma_queue_play_media("player1", "library://track/42", option="add")
            - Play next: ma_queue_play_media("player1", "spotify://track/abc", option="next")
        """
        await client.queue_command(
            queue_id, "play_media", media=media, option=option
        )
        return {"success": True, "queue_id": queue_id, "media": media, "option": option}

    @mcp.tool()
    async def ma_queue_next(queue_id: str) -> dict[str, Any]:
        """Skip to the next track in the queue.

        Args:
            queue_id: The queue to advance.

        Returns:
            Success status.
        """
        await client.queue_command(queue_id, "next")
        return {"success": True, "queue_id": queue_id, "action": "next"}

    @mcp.tool()
    async def ma_queue_previous(queue_id: str) -> dict[str, Any]:
        """Go back to the previous track in the queue.

        Args:
            queue_id: The queue to go back on.

        Returns:
            Success status.
        """
        await client.queue_command(queue_id, "previous")
        return {"success": True, "queue_id": queue_id, "action": "previous"}

    @mcp.tool()
    async def ma_queue_shuffle(
        queue_id: str, shuffle_enabled: bool
    ) -> dict[str, Any]:
        """Enable or disable shuffle mode on a queue.

        Args:
            queue_id: The queue to configure.
            shuffle_enabled: True to enable shuffle, False to disable.

        Returns:
            Success status with the new shuffle setting.
        """
        await client.queue_command(
            queue_id, "shuffle", shuffle_enabled=shuffle_enabled
        )
        return {
            "success": True,
            "queue_id": queue_id,
            "shuffle_enabled": shuffle_enabled,
        }

    @mcp.tool()
    async def ma_queue_repeat(
        queue_id: str, repeat_mode: str
    ) -> dict[str, Any]:
        """Set repeat mode on a queue.

        Args:
            queue_id: The queue to configure.
            repeat_mode: One of:
                - "off": No repeat
                - "one": Repeat the current track
                - "all": Repeat the entire queue

        Returns:
            Success status with the new repeat setting.
        """
        await client.queue_command(
            queue_id, "repeat", repeat_mode=repeat_mode
        )
        return {
            "success": True,
            "queue_id": queue_id,
            "repeat_mode": repeat_mode,
        }

    @mcp.tool()
    async def ma_queue_clear(queue_id: str) -> dict[str, Any]:
        """Clear all items from a queue.

        Args:
            queue_id: The queue to clear.

        Returns:
            Success status.
        """
        await client.queue_command(queue_id, "clear")
        return {"success": True, "queue_id": queue_id, "action": "clear"}

    @mcp.tool()
    async def ma_queue_play_index(
        queue_id: str, index: int
    ) -> dict[str, Any]:
        """Jump to a specific position (index) in the queue.

        Args:
            queue_id: The queue to control.
            index: Zero-based index of the item to play.

        Returns:
            Success status.
        """
        await client.queue_command(queue_id, "play_index", index=index)
        return {"success": True, "queue_id": queue_id, "index": index}

    @mcp.tool()
    async def ma_queue_move_item(
        queue_id: str,
        queue_item_id: str,
        pos_shift: int = 1,
    ) -> dict[str, Any]:
        """Move an item up or down in the queue.

        Args:
            queue_id: The queue containing the item.
            queue_item_id: The unique ID of the queue item to move.
            pos_shift: Number of positions to move. Positive = down, negative = up.

        Returns:
            Success status.
        """
        await client.queue_command(
            queue_id, "move_item", queue_item_id=queue_item_id, pos_shift=pos_shift
        )
        return {
            "success": True,
            "queue_id": queue_id,
            "queue_item_id": queue_item_id,
            "pos_shift": pos_shift,
        }

    @mcp.tool()
    async def ma_queue_delete_item(
        queue_id: str, item_id_or_index: int | str
    ) -> dict[str, Any]:
        """Remove an item from the queue.

        Args:
            queue_id: The queue to remove from.
            item_id_or_index: The queue item ID or index to remove.

        Returns:
            Success status.
        """
        await client.queue_command(
            queue_id, "delete_item", item_id_or_index=item_id_or_index
        )
        return {
            "success": True,
            "queue_id": queue_id,
            "removed": item_id_or_index,
        }

    @mcp.tool()
    async def ma_queue_transfer(
        source_queue_id: str,
        target_queue_id: str,
        auto_play: bool = True,
    ) -> dict[str, Any]:
        """Transfer the current queue from one player to another.

        Moves the queue (including current position and settings) between
        players. Useful for seamlessly continuing playback on a different
        speaker.

        Args:
            source_queue_id: Queue/player to transfer FROM.
            target_queue_id: Queue/player to transfer TO.
            auto_play: Whether to start playing on the target (default True).

        Returns:
            Success status.
        """
        await client.command(
            "player_queues/transfer",
            source_queue_id=source_queue_id,
            target_queue_id=target_queue_id,
            auto_play=auto_play,
        )
        return {
            "success": True,
            "from": source_queue_id,
            "to": target_queue_id,
            "auto_play": auto_play,
        }
