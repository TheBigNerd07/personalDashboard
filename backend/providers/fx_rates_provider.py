from __future__ import annotations

from typing import Any, Dict, List

import httpx

from backend.providers.base import BaseProvider


class FXRatesProvider(BaseProvider):
    name = "fx_rates"

    def __init__(
        self,
        base_currency: str = "USD",
        symbols: List[str] | None = None,
        enabled: bool = True,
        poll_interval: float = 30.0,
        cache_ttl: float = 15.0,
        timeout_s: float = 6.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.base_currency = (base_currency or "USD").upper()
        self.symbols = symbols or ["EUR", "GBP", "JPY", "CAD", "AUD"]
        self.timeout_s = timeout_s

    async def fetch(self) -> Dict[str, Any]:
        url = f"https://open.er-api.com/v6/latest/{self.base_currency}"
        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        rates = raw.get("rates", {}) or {}
        selected = []
        for symbol in self.symbols:
            selected.append(
                {
                    "symbol": symbol,
                    "rate": rates.get(symbol),
                }
            )
        return {
            "base_currency": raw.get("base_code", self.base_currency),
            "updated_utc": raw.get("time_last_update_utc"),
            "rates": selected,
            "source": "open_er_api",
        }
