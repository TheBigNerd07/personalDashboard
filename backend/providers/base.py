from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from backend.models import NormalizedSnapshot


class BaseProvider(ABC):
    """Base contract for all data providers."""

    name: str

    def __init__(self, enabled: bool = True, poll_interval: float = 5.0, cache_ttl: float = 2.0):
        self.enabled = enabled
        self.poll_interval = poll_interval
        self.cache_ttl = cache_ttl

    @abstractmethod
    async def fetch(self) -> Dict[str, Any]:
        """Fetch raw data from the source."""

    @abstractmethod
    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data into a consistent shape."""

    async def run_once(self) -> NormalizedSnapshot:
        raw = await self.fetch()
        normalized = self.normalize(raw)
        return NormalizedSnapshot(source=self.name, status="ok", data=normalized)
