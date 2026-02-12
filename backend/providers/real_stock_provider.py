from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class RealStockProvider(BaseProvider):
    def __init__(
        self,
        symbol: str,
        name: str,
        enabled: bool = True,
        poll_interval: float = 5.0,
        cache_ttl: float = 3.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.name = name
        self.symbol = (symbol or "").strip().upper()
        self.timeout_s = timeout_s
        self._rate_limited_until: datetime | None = None

    async def fetch(self) -> Dict[str, Any]:
        if not self.symbol:
            raise ValueError("Stock symbol is required")

        now = datetime.now(timezone.utc)
        if self._rate_limited_until is not None and now < self._rate_limited_until:
            wait_seconds = int((self._rate_limited_until - now).total_seconds())
            raise RuntimeError(f"Rate limited. Retry in {max(wait_seconds, 1)}s")

        url = "https://query1.finance.yahoo.com/v7/finance/quote"
        params = {"symbols": self.symbol}
        timeout = httpx.Timeout(self.timeout_s)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            if response.status_code in (429, 509):
                retry_after = response.headers.get("Retry-After")
                try:
                    retry_seconds = max(1, min(600, int(retry_after))) if retry_after else 120
                except ValueError:
                    retry_seconds = 120
                self._rate_limited_until = now + timedelta(seconds=retry_seconds)
                if response.status_code == 509:
                    raise RuntimeError(f"Bandwidth limit reached upstream (HTTP 509). Retry in {retry_seconds}s")
                raise RuntimeError(f"Rate limited by upstream (HTTP 429). Retry in {retry_seconds}s")

            response.raise_for_status()
            self._rate_limited_until = None
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        result = (raw.get("quoteResponse", {}).get("result") or [None])[0]
        if not result:
            raise ValueError(f"No quote returned for symbol '{self.symbol}'")

        price = result.get("regularMarketPrice")
        if price is None:
            price = result.get("regularMarketPreviousClose")

        return {
            "quotes": [
                {
                    "symbol": result.get("symbol", self.symbol),
                    "name": result.get("shortName") or result.get("longName"),
                    "exchange": result.get("fullExchangeName") or result.get("exchange"),
                    "currency": result.get("currency"),
                    "price": price,
                    "change_pct": result.get("regularMarketChangePercent"),
                    "open": result.get("regularMarketOpen"),
                    "high": result.get("regularMarketDayHigh"),
                    "low": result.get("regularMarketDayLow"),
                    "volume": result.get("regularMarketVolume"),
                    "market_cap": result.get("marketCap"),
                    "pe_ratio": result.get("trailingPE"),
                    "market_time": result.get("regularMarketTime"),
                    "source": "yahoo_finance",
                }
            ]
        }
