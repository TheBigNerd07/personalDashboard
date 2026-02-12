from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class MarketIndicesProvider(BaseProvider):
    name = "market_indices"

    def __init__(
        self,
        symbols: List[str] | None = None,
        enabled: bool = True,
        poll_interval: float = 12.0,
        cache_ttl: float = 6.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.symbols = symbols or ["^GSPC", "^IXIC", "^DJI", "^VIX"]
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://query1.finance.yahoo.com/v7/finance/quote"
        params = {"symbols": ",".join(self.symbols)}
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        result = raw.get("quoteResponse", {}).get("result", []) or []
        indices = []
        for item in result:
            indices.append(
                {
                    "symbol": item.get("symbol"),
                    "name": item.get("shortName") or item.get("longName"),
                    "price": item.get("regularMarketPrice"),
                    "change": item.get("regularMarketChange"),
                    "change_pct": item.get("regularMarketChangePercent"),
                    "source": "yahoo_finance",
                }
            )
        return {"indices": indices, "count": len(indices)}
