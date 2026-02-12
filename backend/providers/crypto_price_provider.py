from __future__ import annotations

from typing import Any, Dict

import httpx

from backend.providers.base import BaseProvider


class CryptoPriceProvider(BaseProvider):
    name = "crypto_price"

    def __init__(
        self,
        symbol: str = "BTC-USD",
        enabled: bool = True,
        poll_interval: float = 8.0,
        cache_ttl: float = 4.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.symbol = (symbol or "BTC-USD").upper()
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = f"https://api.coinbase.com/v2/prices/{self.symbol}/spot"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        data = raw.get("data", {})
        return {
            "symbol": data.get("base", self.symbol.split("-")[0]),
            "currency": data.get("currency", self.symbol.split("-")[-1]),
            "price": float(data["amount"]) if data.get("amount") is not None else None,
            "source": "coinbase",
        }
