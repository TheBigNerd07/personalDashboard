from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class SolarXrayProvider(BaseProvider):
    name = "solar_xray"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 25.0,
        cache_ttl: float = 10.0,
        timeout_s: float = 8.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return {"series": response.json()}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        series: List[Dict[str, Any]] = raw.get("series", []) or []
        filtered = [row for row in series if row.get("energy") == "0.1-0.8nm"]
        latest = filtered[-1] if filtered else {}
        flux = latest.get("flux")
        return {
            "flux_w_m2": flux,
            "flux_class": latest.get("class"),
            "observed_time": latest.get("time_tag"),
            "source": "noaa_swpc",
        }
