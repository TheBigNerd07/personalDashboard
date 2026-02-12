import asyncio

from backend.providers.base import BaseProvider
from backend.scheduler import DataScheduler


class FakeProvider(BaseProvider):
    name = "fake"

    def __init__(self):
        super().__init__(enabled=True, poll_interval=0.05, cache_ttl=0.4)
        self.calls = 0

    async def fetch(self):
        self.calls += 1
        return {"value": self.calls}

    def normalize(self, raw):
        return raw


def test_scheduler_polls_provider():
    async def runner():
        provider = FakeProvider()
        scheduler = DataScheduler([provider], global_refresh_rate=1.0)

        await scheduler.start()
        await asyncio.sleep(0.18)
        snapshot = scheduler.get_snapshot()
        await scheduler.stop()

        assert provider.calls >= 2
        assert snapshot["sources"][0]["status"] in {"ok", "stale"}

    asyncio.run(runner())


def test_pause_resume():
    async def runner():
        provider = FakeProvider()
        scheduler = DataScheduler([provider], global_refresh_rate=1.0)

        await scheduler.start()
        await asyncio.sleep(0.10)
        await scheduler.pause()
        calls_before_pause = provider.calls
        await asyncio.sleep(0.12)
        calls_after_pause_window = provider.calls
        await scheduler.resume()
        await asyncio.sleep(0.10)
        calls_after_resume = provider.calls
        await scheduler.stop()

        assert calls_after_pause_window <= calls_before_pause + 1
        assert calls_after_resume > calls_after_pause_window

    asyncio.run(runner())


def test_source_controls_and_refresh_now():
    async def runner():
        provider = FakeProvider()
        scheduler = DataScheduler([provider], global_refresh_rate=1.0, history_size=5)

        await scheduler.start()
        await asyncio.sleep(0.12)
        await scheduler.pause_source("fake")
        calls_before = provider.calls
        await asyncio.sleep(0.15)
        calls_after = provider.calls
        assert calls_after <= calls_before + 1

        ok = await scheduler.refresh_now("fake")
        assert ok is True
        assert provider.calls >= calls_after

        snapshot = scheduler.get_snapshot()
        source = snapshot["sources"][0]
        assert source["source_paused"] is True
        assert len(source["history"]) >= 1

        await scheduler.resume_source("fake")
        await asyncio.sleep(0.12)
        await scheduler.stop()

    asyncio.run(runner())
