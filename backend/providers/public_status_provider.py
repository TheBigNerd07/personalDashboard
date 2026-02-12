from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class PublicStatusProvider(BaseProvider):
    name = "public_status"

    def __init__(
        self,
        services: List[Dict[str, Any]],
        enabled: bool = True,
        poll_interval: float = 8.0,
        cache_ttl: float = 4.0,
        timeout_s: float = 5.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.services = services
        self.timeout_s = timeout_s

    async def _check_service(self, client: httpx.AsyncClient, service: Dict[str, Any]) -> Dict[str, Any]:
        name = service.get("name", service.get("url", "unknown"))
        url = service.get("url")
        expect_status = int(service.get("expect_status", 200))

        if not url:
            return {
                "name": name,
                "url": "",
                "ok": False,
                "status_code": None,
                "latency_ms": None,
                "message": "Missing URL",
            }

        start = time.perf_counter()
        try:
            response = await client.get(url, follow_redirects=True)
            latency_ms = round((time.perf_counter() - start) * 1000, 1)
            ok = response.status_code == expect_status
            return {
                "name": name,
                "url": url,
                "ok": ok,
                "status_code": response.status_code,
                "latency_ms": latency_ms,
                "message": "OK" if ok else f"Expected {expect_status}, got {response.status_code}",
            }
        except Exception as exc:
            return {
                "name": name,
                "url": url,
                "ok": False,
                "status_code": None,
                "latency_ms": None,
                "message": str(exc),
            }

    async def fetch(self) -> Dict[str, Any]:
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            checks = await asyncio.gather(*(self._check_service(client, svc) for svc in self.services))
            return {"checks": checks}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        checks = raw.get("checks", [])
        total = len(checks)
        up = len([c for c in checks if c.get("ok")])
        down = total - up
        avg_latency_ms = None
        latencies = [c.get("latency_ms") for c in checks if isinstance(c.get("latency_ms"), (int, float))]
        if latencies:
            avg_latency_ms = round(sum(latencies) / len(latencies), 1)

        return {
            "summary": {
                "total": total,
                "up": up,
                "down": down,
                "avg_latency_ms": avg_latency_ms,
            },
            "services": checks,
        }
