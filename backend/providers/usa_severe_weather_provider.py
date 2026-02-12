from __future__ import annotations

import asyncio
from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


SEVERE_WEATHER_CODES = {95, 96, 99}
SHOWERS_CODES = {80, 81, 82}
SNOW_CODES = {71, 73, 75, 77, 85, 86}


class USASevereWeatherProvider(BaseProvider):
    name = "usa_severe_weather"

    def __init__(
        self,
        cities: List[Dict[str, Any]],
        enabled: bool = True,
        poll_interval: float = 20.0,
        cache_ttl: float = 8.0,
        timeout_s: float = 8.0,
        top_n: int = 8,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.cities = cities
        self.timeout_s = timeout_s
        self.top_n = max(1, top_n)

    async def _fetch_city(self, client: httpx.AsyncClient, city: Dict[str, Any]) -> Dict[str, Any]:
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "current": "temperature_2m,wind_speed_10m,precipitation,weather_code",
            "timezone": "UTC",
        }
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        payload = response.json().get("current", {})
        payload["city"] = city["city"]
        payload["state"] = city.get("state", "")
        return payload

    async def fetch(self) -> Dict[str, Any]:
        if not self.cities:
            return {"cities": []}

        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            results = await asyncio.gather(
                *(self._fetch_city(client, city) for city in self.cities),
                return_exceptions=True,
            )

        parsed = []
        for city, result in zip(self.cities, results):
            if isinstance(result, Exception):
                parsed.append(
                    {
                        "city": city["city"],
                        "state": city.get("state", ""),
                        "error": str(result),
                    }
                )
            else:
                parsed.append(result)

        return {"cities": parsed}

    @staticmethod
    def _score_city(entry: Dict[str, Any]) -> Dict[str, Any]:
        if entry.get("error"):
            return {
                "city": entry.get("city", "Unknown"),
                "state": entry.get("state", ""),
                "severity_score": 0,
                "reason": "No data",
                "weather_code": None,
                "wind_kph": None,
                "precip_mm": None,
                "temperature_c": None,
            }

        code = int(entry.get("weather_code", -1)) if entry.get("weather_code") is not None else -1
        wind_kph = float(entry.get("wind_speed_10m", 0) or 0)
        precip_mm = float(entry.get("precipitation", 0) or 0)
        temp_c = float(entry.get("temperature_2m", 0) or 0)

        score = 0
        reasons: List[str] = []

        if code in SEVERE_WEATHER_CODES:
            score += 60
            reasons.append("thunderstorm")
        elif code in SHOWERS_CODES:
            score += 20
            reasons.append("showers")
        elif code in SNOW_CODES:
            score += 24
            reasons.append("snow")

        if wind_kph >= 55:
            score += 35
            reasons.append("very high wind")
        elif wind_kph >= 40:
            score += 22
            reasons.append("high wind")
        elif wind_kph >= 28:
            score += 12
            reasons.append("gusty wind")

        if precip_mm >= 12:
            score += 30
            reasons.append("heavy precipitation")
        elif precip_mm >= 6:
            score += 18
            reasons.append("moderate precipitation")
        elif precip_mm >= 2:
            score += 8
            reasons.append("light precipitation")

        if temp_c <= -10 or temp_c >= 40:
            score += 20
            reasons.append("temperature extreme")
        elif temp_c <= -2 or temp_c >= 35:
            score += 12
            reasons.append("temperature stress")

        return {
            "city": entry.get("city", "Unknown"),
            "state": entry.get("state", ""),
            "severity_score": int(round(score)),
            "reason": ", ".join(reasons) if reasons else "calm",
            "weather_code": code,
            "wind_kph": round(wind_kph, 1),
            "precip_mm": round(precip_mm, 1),
            "temperature_c": round(temp_c, 1),
        }

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        scored = [self._score_city(entry) for entry in raw.get("cities", [])]
        ranked = sorted(scored, key=lambda item: item["severity_score"], reverse=True)
        worst = ranked[: self.top_n]

        if not worst:
            national_level = "calm"
            national_score = 0
        else:
            national_score = worst[0]["severity_score"]
            if national_score >= 70:
                national_level = "severe"
            elif national_score >= 35:
                national_level = "elevated"
            else:
                national_level = "calm"

        return {
            "national": {
                "severity_level": national_level,
                "peak_score": national_score,
                "monitored_cities": len(scored),
            },
            "worst": worst,
        }
