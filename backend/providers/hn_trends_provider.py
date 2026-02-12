from __future__ import annotations

import asyncio
from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class HNTrendsProvider(BaseProvider):
    name = "hn_trends"

    def __init__(
        self,
        top_n: int = 8,
        enabled: bool = True,
        poll_interval: float = 45.0,
        cache_ttl: float = 20.0,
        timeout_s: float = 8.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.top_n = max(1, top_n)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            ids_response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            ids_response.raise_for_status()
            ids = (ids_response.json() or [])[: self.top_n]

            async def fetch_item(item_id: int) -> Dict[str, Any]:
                item_resp = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
                item_resp.raise_for_status()
                return item_resp.json() or {}

            items = await asyncio.gather(*(fetch_item(item_id) for item_id in ids), return_exceptions=True)
            safe_items: List[Dict[str, Any]] = [item for item in items if isinstance(item, dict)]
            return {"items": safe_items}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        entries = []
        for item in raw.get("items", []):
            entries.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={item.get('id')}",
                    "score": item.get("score"),
                    "comments": item.get("descendants"),
                    "by": item.get("by"),
                }
            )

        return {
            "count": len(entries),
            "stories": entries,
        }
