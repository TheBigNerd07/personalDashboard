from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from backend.providers.base import BaseProvider


class SystemMetricsProvider(BaseProvider):
    name = "system_metrics"

    def __init__(
        self,
        timezones: List[str],
        enabled: bool = True,
        poll_interval: float = 1.0,
        cache_ttl: float = 1.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timezones = timezones

    async def fetch(self) -> Dict[str, Any]:
        now_utc = datetime.now(timezone.utc)
        return {
            "utc": now_utc,
            "timezones": self.timezones,
        }

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        now_utc: datetime = raw["utc"]
        local_now = now_utc.astimezone()

        zones = []
        for tz_name in raw["timezones"]:
            zoned = now_utc.astimezone(ZoneInfo(tz_name))
            zones.append(
                {
                    "timezone": tz_name,
                    "iso": zoned.isoformat(),
                    "time": zoned.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return {
            "utc_iso": now_utc.isoformat(),
            "local_iso": local_now.isoformat(),
            "local_timezone": str(local_now.tzinfo),
            "zones": zones,
        }
