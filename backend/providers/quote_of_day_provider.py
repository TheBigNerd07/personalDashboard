from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class QuoteOfDayProvider(BaseProvider):
    name = "quote_of_day"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 120.0,
        cache_ttl: float = 60.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s
        self._rate_limited_until: datetime | None = None

    async def fetch(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        if self._rate_limited_until is not None and now < self._rate_limited_until:
            wait_seconds = int((self._rate_limited_until - now).total_seconds())
            raise RuntimeError(f"Rate limited. Retry in {max(wait_seconds, 1)}s")

        url = "https://zenquotes.io/api/today"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            if response.status_code in (429, 509):
                retry_after = response.headers.get("Retry-After")
                try:
                    retry_seconds = max(1, min(600, int(retry_after))) if retry_after else 300
                except ValueError:
                    retry_seconds = 300
                self._rate_limited_until = now + timedelta(seconds=retry_seconds)
                if response.status_code == 509:
                    raise RuntimeError(f"Bandwidth limit reached upstream (HTTP 509). Retry in {retry_seconds}s")
                raise RuntimeError(f"Rate limited by upstream (HTTP 429). Retry in {retry_seconds}s")

            response.raise_for_status()
            self._rate_limited_until = None
            return {"items": response.json()}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = raw.get("items", []) or []
        first = items[0] if items else {}
        return {
            "quote": first.get("q"),
            "author": first.get("a"),
            "source": "zenquotes",
        }
