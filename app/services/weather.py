from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


WEATHER_CODE_LABELS = {
    0: "Clear",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Freezing fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy showers",
    95: "Thunderstorm",
}


@dataclass
class WeatherSnapshot:
    available: bool
    temperature: Optional[float] = None
    condition: str = "Unavailable"
    precipitation_chance: Optional[int] = None
    high: Optional[float] = None
    low: Optional[float] = None
    error: Optional[str] = None


def _condition_from_code(code: Any) -> str:
    try:
        return WEATHER_CODE_LABELS.get(int(code), "Unknown")
    except (TypeError, ValueError):
        return "Unknown"


async def fetch_weather(settings: Optional[Settings] = None, client: Optional[httpx.AsyncClient] = None) -> WeatherSnapshot:
    settings = settings or get_settings()
    if not settings.weather_enabled:
        return WeatherSnapshot(available=False, error="Weather is disabled")

    params = {
        "latitude": settings.weather_latitude,
        "longitude": settings.weather_longitude,
        "current": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "temperature_unit": "fahrenheit",
        "timezone": settings.weather_timezone,
    }

    async def _request(active_client: httpx.AsyncClient) -> WeatherSnapshot:
        response = await active_client.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        data = response.json()
        current = data.get("current") or {}
        daily = data.get("daily") or {}
        return WeatherSnapshot(
            available=True,
            temperature=current.get("temperature_2m"),
            condition=_condition_from_code(current.get("weather_code")),
            precipitation_chance=(daily.get("precipitation_probability_max") or [None])[0],
            high=(daily.get("temperature_2m_max") or [None])[0],
            low=(daily.get("temperature_2m_min") or [None])[0],
        )

    try:
        if client is not None:
            return await _request(client)
        async with httpx.AsyncClient(timeout=4.0) as active_client:
            return await _request(active_client)
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError) as exc:
        logger.warning("Weather unavailable: %s", exc)
        return WeatherSnapshot(available=False, error="Weather unavailable")
