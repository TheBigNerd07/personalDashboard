from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class NASAEONETProvider(BaseProvider):
    name = "nasa_events"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 40.0,
        cache_ttl: float = 20.0,
        timeout_s: float = 8.0,
        limit: int = 8,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s
        self.limit = max(1, limit)

    async def fetch(self) -> Dict[str, Any]:
        url = "https://eonet.gsfc.nasa.gov/api/v3/events"
        params = {"status": "open", "limit": self.limit}
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        events: List[Dict[str, Any]] = raw.get("events", []) or []
        items = []
        for event in events:
            geometries = event.get("geometry", []) or []
            latest = geometries[-1] if geometries else {}
            category_list = event.get("categories", []) or []
            items.append(
                {
                    "title": event.get("title"),
                    "category": (category_list[0] or {}).get("title") if category_list else None,
                    "date": latest.get("date"),
                    "source": ((event.get("sources") or [{}])[0]).get("id"),
                }
            )
        return {
            "count": len(items),
            "events": items,
            "source": "nasa_eonet",
        }
