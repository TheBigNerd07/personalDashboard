from __future__ import annotations

import asyncio
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Deque, Dict, List, Optional

from backend.models import NormalizedSnapshot
from backend.providers.base import BaseProvider


@dataclass
class ProviderState:
    provider: BaseProvider
    paused: bool = False
    last_result: Optional[NormalizedSnapshot] = None
    last_success_at: Optional[datetime] = None
    last_attempt_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    history: Deque[NormalizedSnapshot] = field(default_factory=lambda: deque(maxlen=20))


class DataScheduler:
    def __init__(self, providers: List[BaseProvider], global_refresh_rate: float = 1.0, history_size: int = 20):
        self.providers: Dict[str, ProviderState] = {}
        for p in providers:
            if p.enabled:
                state = ProviderState(provider=p)
                state.history = deque(maxlen=max(1, history_size))
                self.providers[p.name] = state

        self.global_refresh_rate = max(0.1, global_refresh_rate)
        self._tasks: List[asyncio.Task] = []
        self._running = False
        self._paused = False
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        for state in self.providers.values():
            self._tasks.append(asyncio.create_task(self._run_provider_loop(state)))

    async def stop(self) -> None:
        self._running = False
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def pause(self) -> None:
        async with self._lock:
            self._paused = True

    async def resume(self) -> None:
        async with self._lock:
            self._paused = False

    async def pause_source(self, source: str) -> bool:
        async with self._lock:
            state = self.providers.get(source)
            if state is None:
                return False
            state.paused = True
            return True

    async def resume_source(self, source: str) -> bool:
        async with self._lock:
            state = self.providers.get(source)
            if state is None:
                return False
            state.paused = False
            return True

    async def refresh_now(self, source: Optional[str] = None) -> bool:
        if source is None:
            await asyncio.gather(*(self._poll_provider(state) for state in self.providers.values()))
            return True

        state = self.providers.get(source)
        if state is None:
            return False
        await self._poll_provider(state)
        return True

    async def set_global_refresh_rate(self, rate: float) -> None:
        async with self._lock:
            self.global_refresh_rate = max(0.1, rate)

    async def _run_provider_loop(self, state: ProviderState) -> None:
        while self._running:
            async with self._lock:
                paused = self._paused
                source_paused = state.paused
                rate = self.global_refresh_rate

            if paused or source_paused:
                await asyncio.sleep(0.1)
                continue

            await self._poll_provider(state)
            wait_s = max(0.1, state.provider.poll_interval / rate)
            state.next_run_at = datetime.now(timezone.utc)
            await asyncio.sleep(wait_s)

    async def _poll_provider(self, state: ProviderState) -> None:
        now = datetime.now(timezone.utc)
        state.last_attempt_at = now
        try:
            result = await state.provider.run_once()
            state.last_result = result
            state.last_success_at = now
            state.history.append(result)
        except Exception as exc:
            previous_data = state.last_result.data if state.last_result else {}
            is_rate_limited = self._is_rate_limited_error(exc)
            status = "stale" if is_rate_limited else "error"
            error_result = NormalizedSnapshot(
                source=state.provider.name,
                status=status,
                data=previous_data,
                error=self._compact_error_message(exc),
            )
            state.last_result = error_result
            state.history.append(error_result)

    @staticmethod
    def _is_rate_limited_error(exc: Exception) -> bool:
        text = str(exc).lower()
        return "rate limit" in text or "429" in text

    @staticmethod
    def _compact_error_message(exc: Exception) -> str:
        text = str(exc).strip()
        if not text:
            return "Request failed"

        lower = text.lower()
        if "rate limit" in lower or "429" in lower:
            retry = re.search(r"retry\s+(?:after|in)\s+(\d+)\s*s", lower)
            if retry:
                return f"Rate limited. Retry in {retry.group(1)}s"
            return "Rate limited by upstream (HTTP 429)"

        if len(text) > 220:
            return f"{text[:217]}..."
        return text

    def get_snapshot(self) -> Dict[str, object]:
        now = datetime.now(timezone.utc)
        sources = []

        for name, state in self.providers.items():
            result = state.last_result
            if result is None:
                sources.append(
                    {
                        "source": name,
                        "status": "stale",
                        "source_paused": state.paused,
                        "data": {},
                        "fetched_at": None,
                        "error": "No data yet",
                        "poll_interval": state.provider.poll_interval,
                        "history": [],
                    }
                )
                continue

            status = result.status
            if status == "ok" and state.last_success_at is not None:
                age = (now - state.last_success_at).total_seconds()
                if age > state.provider.cache_ttl:
                    status = "stale"

            sources.append(
                {
                    "source": result.source,
                    "status": status,
                    "source_paused": state.paused,
                    "data": result.data,
                    "fetched_at": result.fetched_at.isoformat(),
                    "error": result.error,
                    "poll_interval": state.provider.poll_interval,
                    "history": [
                        {
                            "status": item.status,
                            "fetched_at": item.fetched_at.isoformat(),
                            "data": item.data,
                        }
                        for item in state.history
                    ],
                }
            )

        return {
            "paused": self._paused,
            "global_refresh_rate": self.global_refresh_rate,
            "generated_at": now.isoformat(),
            "source_count": len(sources),
            "sources": sources,
        }
