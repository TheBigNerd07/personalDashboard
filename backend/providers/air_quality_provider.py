from __future__ import annotations

from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class AirQualityProvider(BaseProvider):
    name = "air_quality"

    def __init__(
        self,
        latitude: float = 47.6588,
        longitude: float = -117.4260,
        enabled: bool = True,
        poll_interval: float = 25.0,
        cache_ttl: float = 10.0,
        timeout_s: float = 8.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.latitude = latitude
        self.longitude = longitude
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "us_aqi,pm2_5,pm10,ozone",
            "timezone": "UTC",
        }
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        current = raw.get("current", {}) or {}
        return {
            "aqi_us": current.get("us_aqi"),
            "pm2_5": current.get("pm2_5"),
            "pm10": current.get("pm10"),
            "ozone": current.get("ozone"),
            "source": "open_meteo",
        }
