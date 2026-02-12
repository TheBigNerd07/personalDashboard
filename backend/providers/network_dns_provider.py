from __future__ import annotations

import socket
from typing import Any, Dict, List

from backend.providers.base import BaseProvider


class NetworkDNSProvider(BaseProvider):
    name = "network_dns"

    def __init__(
        self,
        hosts: List[str] | None = None,
        enabled: bool = True,
        poll_interval: float = 35.0,
        cache_ttl: float = 15.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.hosts = hosts or ["api.github.com", "query1.finance.yahoo.com", "api.open-meteo.com"]

    async def fetch(self) -> Dict[str, Any]:
        results = []
        for host in self.hosts:
            try:
                _, _, addresses = socket.gethostbyname_ex(host)
                results.append({"host": host, "ok": True, "addresses": addresses})
            except OSError as exc:
                results.append({"host": host, "ok": False, "addresses": [], "error": str(exc)})
        return {"results": results}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        checks = raw.get("results", []) or []
        ok = sum(1 for check in checks if check.get("ok"))
        return {
            "summary": {
                "ok": ok,
                "total": len(checks),
                "down": len(checks) - ok,
            },
            "checks": checks,
        }
