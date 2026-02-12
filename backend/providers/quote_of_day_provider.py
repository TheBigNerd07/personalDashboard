from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class QuoteOfDayProvider(BaseProvider):
    name = "quote_of_day"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 120.0,
        cache_ttl: float = 60.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://zenquotes.io/api/today"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return {"items": response.json()}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = raw.get("items", []) or []
        first = items[0] if items else {}
        return {
            "quote": first.get("q"),
            "author": first.get("a"),
            "source": "zenquotes",
        }
