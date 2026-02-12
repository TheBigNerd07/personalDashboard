from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class EarthquakeProvider(BaseProvider):
    name = "earthquakes"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 30.0,
        cache_ttl: float = 12.0,
        timeout_s: float = 7.0,
        max_events: int = 6,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s
        self.max_events = max(1, max_events)

    async def fetch(self) -> Dict[str, Any]:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        features: List[Dict[str, Any]] = raw.get("features", []) or []
        events = []
        mags = []
        for feature in features[: self.max_events]:
            props = feature.get("properties", {}) or {}
            mag = props.get("mag")
            if isinstance(mag, (float, int)):
                mags.append(float(mag))
            events.append(
                {
                    "place": props.get("place"),
                    "mag": mag,
                    "time_ms": props.get("time"),
                    "url": props.get("url"),
                }
            )
        return {
            "count_last_hour": len(features),
            "max_magnitude": max(mags) if mags else None,
            "events": events,
            "source": "usgs",
        }
