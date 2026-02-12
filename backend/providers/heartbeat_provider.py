from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Dict

from backend.providers.base import BaseProvider


class HeartbeatProvider(BaseProvider):
    name = "heartbeat"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 1.0,
        cache_ttl: float = 1.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.started_monotonic = time.monotonic()

    async def fetch(self) -> Dict[str, Any]:
        now_utc = datetime.now(timezone.utc)
        uptime_seconds = round(time.monotonic() - self.started_monotonic, 1)
        return {
            "utc_now": now_utc,
            "uptime_seconds": uptime_seconds,
            "heartbeat": "alive",
        }

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "heartbeat": raw.get("heartbeat", "unknown"),
            "utc_now": raw["utc_now"].isoformat() if raw.get("utc_now") else None,
            "uptime_seconds": raw.get("uptime_seconds"),
        }
