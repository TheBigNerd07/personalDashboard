from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class SpaceWeatherProvider(BaseProvider):
    name = "space_weather"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 20.0,
        cache_ttl: float = 10.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return {"series": response.json()}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        series: List[Dict[str, Any]] = raw.get("series", []) or []
        latest = series[-1] if series else {}
        kp = latest.get("kp_index")
        level = "quiet"
        if isinstance(kp, (float, int)):
            if kp >= 5:
                level = "storm"
            elif kp >= 4:
                level = "active"
            elif kp >= 3:
                level = "unsettled"
        return {
            "kp_index": kp,
            "level": level,
            "observed_time": latest.get("time_tag"),
            "source": "noaa_swpc",
        }
