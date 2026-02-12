from __future__ import annotations

from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class MempoolFeesProvider(BaseProvider):
    name = "mempool_fees"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 15.0,
        cache_ttl: float = 8.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://mempool.space/api/v1/fees/recommended"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "fastest_sat_vb": raw.get("fastestFee"),
            "half_hour_sat_vb": raw.get("halfHourFee"),
            "hour_sat_vb": raw.get("hourFee"),
            "minimum_sat_vb": raw.get("minimumFee"),
            "economy_sat_vb": raw.get("economyFee"),
            "source": "mempool_space",
        }
