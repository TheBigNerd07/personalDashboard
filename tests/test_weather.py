from __future__ import annotations

import asyncio

import httpx

from app.config import Settings
from app.services.weather import fetch_weather


class FailingWeatherClient:
    async def get(self, url: str, params: dict):
        raise httpx.ConnectError("offline")


def test_weather_failure_returns_unavailable_snapshot():
    settings = Settings(
        app_name="Command Center",
        app_password="",
        secret_key="test",
        database_url="sqlite:///:memory:",
        llm_enabled=False,
        llm_base_url="http://example.test/v1",
        llm_model="local-model",
        llm_timeout_seconds=8,
        weather_enabled=True,
        weather_latitude=47.712,
        weather_longitude=-116.948,
        weather_timezone="America/Los_Angeles",
    )

    snapshot = asyncio.run(fetch_weather(settings, client=FailingWeatherClient()))

    assert snapshot.available is False
    assert snapshot.error == "Weather unavailable"

