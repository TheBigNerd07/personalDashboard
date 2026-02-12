from __future__ import annotations

import random
from typing import Any, Dict, List

from backend.providers.base import BaseProvider


class MockMarketProvider(BaseProvider):
    name = "mock_market"

    def __init__(
        self,
        symbols: List[str],
        name: str = "mock_market",
        enabled: bool = True,
        poll_interval: float = 2.0,
        cache_ttl: float = 1.5,
        seed: int | None = None,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.name = name
        self.random = random.Random(seed)
        self.prices = {symbol: round(self.random.uniform(20.0, 250.0), 2) for symbol in symbols}
        self.sessions = {
            symbol: {
                "open": price,
                "high": price,
                "low": price,
                "volume": self.random.randint(150_000, 1_500_000),
            }
            for symbol, price in self.prices.items()
        }

    async def fetch(self) -> Dict[str, Any]:
        updates = {}
        for symbol, price in self.prices.items():
            pct_move = self.random.uniform(-0.02, 0.02)
            next_price = max(1.0, price * (1 + pct_move))
            self.prices[symbol] = round(next_price, 2)
            session = self.sessions[symbol]
            session["high"] = round(max(session["high"], self.prices[symbol]), 2)
            session["low"] = round(min(session["low"], self.prices[symbol]), 2)
            session["volume"] += self.random.randint(5_000, 90_000)
            updates[symbol] = {
                "price": self.prices[symbol],
                "change_pct": round(pct_move * 100, 3),
                "open": session["open"],
                "high": session["high"],
                "low": session["low"],
                "volume": session["volume"],
            }
        return {"quotes": updates}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        quotes = raw.get("quotes", {})
        return {
            "quotes": [
                {
                    "symbol": symbol,
                    "price": details["price"],
                    "change_pct": details["change_pct"],
                    "open": details.get("open"),
                    "high": details.get("high"),
                    "low": details.get("low"),
                    "volume": details.get("volume"),
                }
                for symbol, details in sorted(quotes.items())
            ]
        }
