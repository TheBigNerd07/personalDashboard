from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class SunTimesProvider(BaseProvider):
    name = "sun_times"

    def __init__(
        self,
        latitude: float = 47.6588,
        longitude: float = -117.4260,
        enabled: bool = True,
        poll_interval: float = 90.0,
        cache_ttl: float = 60.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.latitude = latitude
        self.longitude = longitude
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://api.sunrise-sunset.org/json"
        params = {
            "lat": self.latitude,
            "lng": self.longitude,
            "formatted": 0,
        }
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        results = raw.get("results", {}) or {}

        def parse_dt(value: Any) -> datetime | None:
            if not isinstance(value, str):
                return None
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None

        sunrise = parse_dt(results.get("sunrise"))
        sunset = parse_dt(results.get("sunset"))
        daylight_hours = None
        if sunrise and sunset:
            daylight_hours = round((sunset - sunrise).total_seconds() / 3600, 2)

        return {
            "sunrise_utc": sunrise.isoformat() if sunrise else None,
            "sunset_utc": sunset.isoformat() if sunset else None,
            "day_length_hours": daylight_hours,
            "solar_noon_utc": results.get("solar_noon"),
        }
