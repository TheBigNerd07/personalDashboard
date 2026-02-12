from __future__ import annotations

from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class CryptoGlobalProvider(BaseProvider):
    name = "crypto_global"

    def __init__(
        self,
        enabled: bool = True,
        poll_interval: float = 20.0,
        cache_ttl: float = 10.0,
        timeout_s: float = 8.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = "https://api.coingecko.com/api/v3/global"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        data = raw.get("data", {}) or {}
        return {
            "active_cryptocurrencies": data.get("active_cryptocurrencies"),
            "markets": data.get("markets"),
            "total_market_cap_usd": (data.get("total_market_cap") or {}).get("usd"),
            "total_volume_usd": (data.get("total_volume") or {}).get("usd"),
            "btc_dominance_pct": (data.get("market_cap_percentage") or {}).get("btc"),
            "eth_dominance_pct": (data.get("market_cap_percentage") or {}).get("eth"),
            "source": "coingecko",
        }
