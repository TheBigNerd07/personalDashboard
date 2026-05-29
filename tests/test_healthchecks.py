from __future__ import annotations

import asyncio

import httpx

from app.services.healthchecks import check_health_url


class FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class HealthyClient:
    async def get(self, url: str):
        return FakeResponse(204)


class FailingClient:
    async def get(self, url: str):
        raise httpx.ConnectError("offline")


def test_healthcheck_without_url_is_unknown():
    result = asyncio.run(check_health_url(None))
    assert result.status == "unknown"


def test_healthcheck_success_is_up():
    result = asyncio.run(check_health_url("http://service.local/health", client=HealthyClient()))
    assert result.status == "up"


def test_healthcheck_connection_error_is_down():
    result = asyncio.run(check_health_url("http://service.local/health", client=FailingClient()))
    assert result.status == "down"

