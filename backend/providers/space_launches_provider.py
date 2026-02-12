from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class SpaceLaunchesProvider(BaseProvider):
    name = "space_launches"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 60.0,
        cache_ttl: float = 30.0,
        timeout_s: float = 8.0,
        limit: int = 6,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s
        self.limit = max(1, limit)

    async def fetch(self) -> Dict[str, Any]:
        url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
        params = {"limit": self.limit}
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = raw.get("results", []) or []
        launches = []
        for item in results:
            launches.append(
                {
                    "name": item.get("name"),
                    "window_start": item.get("window_start"),
                    "status": (item.get("status") or {}).get("name"),
                    "provider": ((item.get("launch_service_provider") or {}).get("name")),
                    "location": (((item.get("pad") or {}).get("location") or {}).get("name")),
                    "mission": ((item.get("mission") or {}).get("name")),
                }
            )
        return {
            "count": len(launches),
            "launches": launches,
            "source": "thespacedevs",
        }
