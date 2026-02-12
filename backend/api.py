from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.config import DEFAULT_CONFIG_PATH, load_config, save_config
from backend.providers.base import BaseProvider
from backend.providers.air_quality_provider import AirQualityProvider
from backend.providers.crypto_price_provider import CryptoPriceProvider
from backend.providers.crypto_global_provider import CryptoGlobalProvider
from backend.providers.earthquake_provider import EarthquakeProvider
from backend.providers.fx_rates_provider import FXRatesProvider
from backend.providers.heartbeat_provider import HeartbeatProvider
from backend.providers.hn_trends_provider import HNTrendsProvider
from backend.providers.iss_position_provider import ISSPositionProvider
from backend.providers.market_indices_provider import MarketIndicesProvider
from backend.providers.mempool_fees_provider import MempoolFeesProvider
from backend.providers.nasa_eonet_provider import NASAEONETProvider
from backend.providers.network_dns_provider import NetworkDNSProvider
from backend.providers.public_status_provider import PublicStatusProvider
from backend.providers.quote_of_day_provider import QuoteOfDayProvider
from backend.providers.real_stock_provider import RealStockProvider
from backend.providers.solar_xray_provider import SolarXrayProvider
from backend.providers.space_launches_provider import SpaceLaunchesProvider
from backend.providers.space_weather_provider import SpaceWeatherProvider
from backend.providers.sun_times_provider import SunTimesProvider
from backend.providers.system_metrics_provider import SystemMetricsProvider
from backend.providers.travel_time_provider import TravelTimeProvider
from backend.providers.usa_severe_weather_provider import USASevereWeatherProvider
from backend.providers.weather_provider import WeatherProvider
from backend.providers.youtube_subscriptions_provider import YouTubeSubscriptionsProvider
from backend.scheduler import DataScheduler


class RefreshRequest(BaseModel):
    global_refresh_rate: float = Field(..., gt=0)


class RefreshNowRequest(BaseModel):
    source: Optional[str] = None


def build_providers(cfg: Dict[str, Any]) -> List[BaseProvider]:
    providers: List[BaseProvider] = []
    provider_cfg = cfg.get("providers", {})

    weather_cfg = provider_cfg.get("weather", {})
    providers.append(
        WeatherProvider(
            city=weather_cfg.get("city", "Seattle"),
            latitude=weather_cfg.get("latitude", 47.6062),
            longitude=weather_cfg.get("longitude", -122.3321),
            enabled=weather_cfg.get("enabled", True),
            poll_interval=float(weather_cfg.get("poll_interval", 10)),
            cache_ttl=float(weather_cfg.get("cache_ttl", 3)),
        )
    )

    time_cfg = provider_cfg.get("system_metrics", provider_cfg.get("time", {}))
    providers.append(
        SystemMetricsProvider(
            timezones=time_cfg.get("timezones", ["UTC", "America/New_York", "America/Los_Angeles"]),
            enabled=time_cfg.get("enabled", True),
            poll_interval=float(time_cfg.get("poll_interval", 1)),
            cache_ttl=float(time_cfg.get("cache_ttl", 1)),
        )
    )

    legacy_market_cfg = provider_cfg.get("mock_market", {})
    legacy_symbols = legacy_market_cfg.get("symbols", ["AAPL", "MSFT", "NVDA"])
    stock_defaults = [
        ("stock_1", "AAPL"),
        ("stock_2", "MSFT"),
        ("stock_3", "NVDA"),
    ]
    for idx, (stock_name, fallback_symbol) in enumerate(stock_defaults):
        stock_cfg = provider_cfg.get(stock_name, {})
        default_symbol = legacy_symbols[idx] if idx < len(legacy_symbols) else fallback_symbol
        providers.append(
            RealStockProvider(
                name=stock_name,
                symbol=str(stock_cfg.get("symbol", default_symbol)).upper(),
                enabled=stock_cfg.get("enabled", legacy_market_cfg.get("enabled", True)),
                poll_interval=float(stock_cfg.get("poll_interval", legacy_market_cfg.get("poll_interval", 2))),
                cache_ttl=float(stock_cfg.get("cache_ttl", legacy_market_cfg.get("cache_ttl", 2))),
                timeout_s=float(stock_cfg.get("timeout_s", 6)),
            )
        )

    status_cfg = provider_cfg.get("public_status", {})
    providers.append(
        PublicStatusProvider(
            services=status_cfg.get(
                "services",
                [
                    {"name": "GitHub API", "url": "https://api.github.com", "expect_status": 200},
                    {
                        "name": "Open-Meteo API",
                        "url": "https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0",
                        "expect_status": 200,
                    },
                ],
            ),
            enabled=status_cfg.get("enabled", True),
            poll_interval=float(status_cfg.get("poll_interval", 8)),
            cache_ttl=float(status_cfg.get("cache_ttl", 4)),
            timeout_s=float(status_cfg.get("timeout_s", 5)),
        )
    )

    heartbeat_cfg = provider_cfg.get("heartbeat", {})
    providers.append(
        HeartbeatProvider(
            enabled=heartbeat_cfg.get("enabled", True),
            poll_interval=float(heartbeat_cfg.get("poll_interval", 1)),
            cache_ttl=float(heartbeat_cfg.get("cache_ttl", 1)),
        )
    )

    severe_cfg = provider_cfg.get("usa_severe_weather", {})
    providers.append(
        USASevereWeatherProvider(
            cities=severe_cfg.get(
                "cities",
                [
                    {"city": "Seattle", "state": "WA", "latitude": 47.6062, "longitude": -122.3321},
                    {"city": "San Francisco", "state": "CA", "latitude": 37.7749, "longitude": -122.4194},
                    {"city": "Los Angeles", "state": "CA", "latitude": 34.0522, "longitude": -118.2437},
                    {"city": "Denver", "state": "CO", "latitude": 39.7392, "longitude": -104.9903},
                    {"city": "Dallas", "state": "TX", "latitude": 32.7767, "longitude": -96.7970},
                    {"city": "Chicago", "state": "IL", "latitude": 41.8781, "longitude": -87.6298},
                    {"city": "Atlanta", "state": "GA", "latitude": 33.7490, "longitude": -84.3880},
                    {"city": "Miami", "state": "FL", "latitude": 25.7617, "longitude": -80.1918},
                    {"city": "New York", "state": "NY", "latitude": 40.7128, "longitude": -74.0060},
                    {"city": "Boston", "state": "MA", "latitude": 42.3601, "longitude": -71.0589},
                ],
            ),
            enabled=severe_cfg.get("enabled", True),
            poll_interval=float(severe_cfg.get("poll_interval", 20)),
            cache_ttl=float(severe_cfg.get("cache_ttl", 8)),
            timeout_s=float(severe_cfg.get("timeout_s", 8)),
            top_n=int(severe_cfg.get("top_n", 8)),
        )
    )

    youtube_cfg = provider_cfg.get("youtube_subscriptions", {})
    providers.append(
        YouTubeSubscriptionsProvider(
            channel_ids=youtube_cfg.get("channel_ids", []),
            enabled=youtube_cfg.get("enabled", False),
            poll_interval=float(youtube_cfg.get("poll_interval", 60)),
            cache_ttl=float(youtube_cfg.get("cache_ttl", 20)),
            timeout_s=float(youtube_cfg.get("timeout_s", 8)),
            max_videos=int(youtube_cfg.get("max_videos", 15)),
        )
    )

    travel_cfg = provider_cfg.get("travel_time", {})
    providers.append(
        TravelTimeProvider(
            origin=travel_cfg.get(
                "origin",
                {"name": "Home", "address": "Spokane, WA"},
            ),
            destinations=travel_cfg.get(
                "destinations",
                [
                    {"name": "Downtown", "address": "Downtown Spokane, WA"},
                    {"name": "Airport", "address": "Spokane International Airport"},
                    {"name": "Office", "address": "Spokane Valley, WA"},
                ],
            ),
            enabled=travel_cfg.get("enabled", False),
            poll_interval=float(travel_cfg.get("poll_interval", 45)),
            cache_ttl=float(travel_cfg.get("cache_ttl", 20)),
            timeout_s=float(travel_cfg.get("timeout_s", 8)),
        )
    )

    crypto_cfg = provider_cfg.get("crypto_price", {})
    providers.append(
        CryptoPriceProvider(
            symbol=crypto_cfg.get("symbol", "BTC-USD"),
            enabled=crypto_cfg.get("enabled", True),
            poll_interval=float(crypto_cfg.get("poll_interval", 8)),
            cache_ttl=float(crypto_cfg.get("cache_ttl", 4)),
            timeout_s=float(crypto_cfg.get("timeout_s", 6)),
        )
    )

    hn_cfg = provider_cfg.get("hn_trends", {})
    providers.append(
        HNTrendsProvider(
            top_n=int(hn_cfg.get("top_n", 8)),
            enabled=hn_cfg.get("enabled", True),
            poll_interval=float(hn_cfg.get("poll_interval", 45)),
            cache_ttl=float(hn_cfg.get("cache_ttl", 20)),
            timeout_s=float(hn_cfg.get("timeout_s", 8)),
        )
    )

    eq_cfg = provider_cfg.get("earthquakes", {})
    providers.append(
        EarthquakeProvider(
            enabled=eq_cfg.get("enabled", True),
            poll_interval=float(eq_cfg.get("poll_interval", 30)),
            cache_ttl=float(eq_cfg.get("cache_ttl", 12)),
            timeout_s=float(eq_cfg.get("timeout_s", 7)),
            max_events=int(eq_cfg.get("max_events", 6)),
        )
    )

    sun_cfg = provider_cfg.get("sun_times", {})
    providers.append(
        SunTimesProvider(
            latitude=float(sun_cfg.get("latitude", 47.6588)),
            longitude=float(sun_cfg.get("longitude", -117.4260)),
            enabled=sun_cfg.get("enabled", True),
            poll_interval=float(sun_cfg.get("poll_interval", 90)),
            cache_ttl=float(sun_cfg.get("cache_ttl", 60)),
            timeout_s=float(sun_cfg.get("timeout_s", 6)),
        )
    )

    air_cfg = provider_cfg.get("air_quality", {})
    providers.append(
        AirQualityProvider(
            latitude=float(air_cfg.get("latitude", 47.6588)),
            longitude=float(air_cfg.get("longitude", -117.4260)),
            enabled=air_cfg.get("enabled", True),
            poll_interval=float(air_cfg.get("poll_interval", 25)),
            cache_ttl=float(air_cfg.get("cache_ttl", 10)),
            timeout_s=float(air_cfg.get("timeout_s", 8)),
        )
    )

    iss_cfg = provider_cfg.get("iss_position", {})
    providers.append(
        ISSPositionProvider(
            enabled=iss_cfg.get("enabled", True),
            poll_interval=float(iss_cfg.get("poll_interval", 5)),
            cache_ttl=float(iss_cfg.get("cache_ttl", 3)),
            timeout_s=float(iss_cfg.get("timeout_s", 5)),
        )
    )

    dns_cfg = provider_cfg.get("network_dns", {})
    providers.append(
        NetworkDNSProvider(
            hosts=dns_cfg.get("hosts", ["api.github.com", "query1.finance.yahoo.com", "api.open-meteo.com"]),
            enabled=dns_cfg.get("enabled", True),
            poll_interval=float(dns_cfg.get("poll_interval", 35)),
            cache_ttl=float(dns_cfg.get("cache_ttl", 15)),
        )
    )

    indices_cfg = provider_cfg.get("market_indices", {})
    providers.append(
        MarketIndicesProvider(
            symbols=indices_cfg.get("symbols", ["^GSPC", "^IXIC", "^DJI", "^VIX"]),
            enabled=indices_cfg.get("enabled", True),
            poll_interval=float(indices_cfg.get("poll_interval", 12)),
            cache_ttl=float(indices_cfg.get("cache_ttl", 6)),
            timeout_s=float(indices_cfg.get("timeout_s", 6)),
        )
    )

    fx_cfg = provider_cfg.get("fx_rates", {})
    providers.append(
        FXRatesProvider(
            base_currency=fx_cfg.get("base_currency", "USD"),
            symbols=fx_cfg.get("symbols", ["EUR", "GBP", "JPY", "CAD", "AUD"]),
            enabled=fx_cfg.get("enabled", True),
            poll_interval=float(fx_cfg.get("poll_interval", 30)),
            cache_ttl=float(fx_cfg.get("cache_ttl", 15)),
            timeout_s=float(fx_cfg.get("timeout_s", 6)),
        )
    )

    space_cfg = provider_cfg.get("space_weather", {})
    providers.append(
        SpaceWeatherProvider(
            enabled=space_cfg.get("enabled", True),
            poll_interval=float(space_cfg.get("poll_interval", 20)),
            cache_ttl=float(space_cfg.get("cache_ttl", 10)),
            timeout_s=float(space_cfg.get("timeout_s", 6)),
        )
    )

    quote_cfg = provider_cfg.get("quote_of_day", {})
    providers.append(
        QuoteOfDayProvider(
            enabled=quote_cfg.get("enabled", True),
            poll_interval=float(quote_cfg.get("poll_interval", 120)),
            cache_ttl=float(quote_cfg.get("cache_ttl", 60)),
            timeout_s=float(quote_cfg.get("timeout_s", 6)),
        )
    )

    mempool_cfg = provider_cfg.get("mempool_fees", {})
    providers.append(
        MempoolFeesProvider(
            enabled=mempool_cfg.get("enabled", True),
            poll_interval=float(mempool_cfg.get("poll_interval", 15)),
            cache_ttl=float(mempool_cfg.get("cache_ttl", 8)),
            timeout_s=float(mempool_cfg.get("timeout_s", 6)),
        )
    )

    eonet_cfg = provider_cfg.get("nasa_events", {})
    providers.append(
        NASAEONETProvider(
            enabled=eonet_cfg.get("enabled", True),
            poll_interval=float(eonet_cfg.get("poll_interval", 40)),
            cache_ttl=float(eonet_cfg.get("cache_ttl", 20)),
            timeout_s=float(eonet_cfg.get("timeout_s", 8)),
            limit=int(eonet_cfg.get("limit", 8)),
        )
    )

    xray_cfg = provider_cfg.get("solar_xray", {})
    providers.append(
        SolarXrayProvider(
            enabled=xray_cfg.get("enabled", True),
            poll_interval=float(xray_cfg.get("poll_interval", 25)),
            cache_ttl=float(xray_cfg.get("cache_ttl", 10)),
            timeout_s=float(xray_cfg.get("timeout_s", 8)),
        )
    )

    crypto_global_cfg = provider_cfg.get("crypto_global", {})
    providers.append(
        CryptoGlobalProvider(
            enabled=crypto_global_cfg.get("enabled", True),
            poll_interval=float(crypto_global_cfg.get("poll_interval", 20)),
            cache_ttl=float(crypto_global_cfg.get("cache_ttl", 10)),
            timeout_s=float(crypto_global_cfg.get("timeout_s", 8)),
        )
    )

    launches_cfg = provider_cfg.get("space_launches", {})
    providers.append(
        SpaceLaunchesProvider(
            enabled=launches_cfg.get("enabled", True),
            poll_interval=float(launches_cfg.get("poll_interval", 60)),
            cache_ttl=float(launches_cfg.get("cache_ttl", 30)),
            timeout_s=float(launches_cfg.get("timeout_s", 8)),
            limit=int(launches_cfg.get("limit", 6)),
        )
    )

    return providers


def _validate_settings(cfg: Dict[str, Any]) -> None:
    if not isinstance(cfg, dict):
        raise HTTPException(status_code=400, detail="Settings must be a JSON object")
    providers = cfg.get("providers")
    if not isinstance(providers, dict):
        raise HTTPException(status_code=400, detail="'providers' must be an object")


def _build_scheduler(cfg: Dict[str, Any]) -> DataScheduler:
    return DataScheduler(
        providers=build_providers(cfg),
        global_refresh_rate=float(cfg.get("global_refresh_rate", 1.0)),
        history_size=int(cfg.get("history_size", 20)),
    )


CONFIG_PATH = DEFAULT_CONFIG_PATH
config: Dict[str, Any] = load_config(CONFIG_PATH)
scheduler = _build_scheduler(config)
settings_lock = asyncio.Lock()

app = FastAPI(title="Real-Time Data Monitor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    await scheduler.start()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await scheduler.stop()


@app.get("/api/settings")
async def get_settings() -> Dict[str, Any]:
    return {"config": config}


@app.post("/api/settings")
async def update_settings(payload: Dict[str, Any]) -> Dict[str, Any]:
    global config
    global scheduler

    _validate_settings(payload)

    async with settings_lock:
        old_scheduler = scheduler
        new_config = payload
        new_scheduler = _build_scheduler(new_config)

        await new_scheduler.start()
        await old_scheduler.stop()

        config = new_config
        scheduler = new_scheduler
        save_config(config, CONFIG_PATH)

    return {"updated": True, "source_count": len(scheduler.providers)}


@app.get("/api/snapshot")
async def get_snapshot() -> Dict[str, object]:
    snapshot = scheduler.get_snapshot()
    snapshot["unit_system"] = str(config.get("unit_system", "metric")).lower()
    snapshot["brand_palette"] = str(config.get("brand_palette", "fleet")).lower()
    snapshot["appearance_mode"] = str(config.get("appearance_mode", "light")).lower()
    snapshot["theme"] = config.get("theme", {})
    return snapshot


@app.post("/api/pause")
async def pause_updates() -> Dict[str, object]:
    await scheduler.pause()
    return {"paused": True}


@app.post("/api/resume")
async def resume_updates() -> Dict[str, object]:
    await scheduler.resume()
    return {"paused": False}


@app.post("/api/refresh-rate")
async def set_refresh_rate(payload: RefreshRequest) -> Dict[str, object]:
    await scheduler.set_global_refresh_rate(payload.global_refresh_rate)
    return {"global_refresh_rate": payload.global_refresh_rate}


@app.post("/api/refresh-now")
async def refresh_now(payload: RefreshNowRequest) -> Dict[str, object]:
    ok = await scheduler.refresh_now(source=payload.source)
    if not ok:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"refreshed": payload.source or "all"}


@app.post("/api/source/{source}/pause")
async def pause_source(source: str) -> Dict[str, object]:
    ok = await scheduler.pause_source(source)
    if not ok:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source": source, "paused": True}


@app.post("/api/source/{source}/resume")
async def resume_source(source: str) -> Dict[str, object]:
    ok = await scheduler.resume_source(source)
    if not ok:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source": source, "paused": False}


@app.get("/")
async def dashboard() -> FileResponse:
    index_path = Path("frontend/index.html")
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


@app.get("/styles.css")
async def styles() -> FileResponse:
    path = Path("frontend/styles.css")
    if not path.exists():
        raise HTTPException(status_code=404, detail="styles.css not found")
    return FileResponse(path)


@app.get("/app.js")
async def app_js() -> FileResponse:
    path = Path("frontend/app.js")
    if not path.exists():
        raise HTTPException(status_code=404, detail="app.js not found")
    return FileResponse(path)
