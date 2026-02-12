from __future__ import annotations

from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class ISSPositionProvider(BaseProvider):
    name = "iss_position"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 5.0,
        cache_ttl: float = 3.0,
        timeout_s: float = 5.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "http://api.open-notify.org/iss-now.json"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        position = raw.get("iss_position", {}) or {}
        return {
            "latitude": float(position.get("latitude")) if position.get("latitude") is not None else None,
            "longitude": float(position.get("longitude")) if position.get("longitude") is not None else None,
            "timestamp": raw.get("timestamp"),
            "message": raw.get("message"),
            "source": "open_notify",
        }
