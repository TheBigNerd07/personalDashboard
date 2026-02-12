from datetime import datetime, timezone
import asyncio
import httpx

from backend.providers.mock_market_provider import MockMarketProvider
from backend.providers.public_status_provider import PublicStatusProvider
from backend.providers.real_stock_provider import RealStockProvider
from backend.providers.market_indices_provider import MarketIndicesProvider
from backend.providers.fx_rates_provider import FXRatesProvider
from backend.providers.space_weather_provider import SpaceWeatherProvider
from backend.providers.quote_of_day_provider import QuoteOfDayProvider
from backend.providers.mempool_fees_provider import MempoolFeesProvider
from backend.providers.nasa_eonet_provider import NASAEONETProvider
from backend.providers.solar_xray_provider import SolarXrayProvider
from backend.providers.crypto_global_provider import CryptoGlobalProvider
from backend.providers.space_launches_provider import SpaceLaunchesProvider
from backend.providers.heartbeat_provider import HeartbeatProvider
from backend.providers.system_metrics_provider import SystemMetricsProvider
from backend.providers.usa_severe_weather_provider import USASevereWeatherProvider
from backend.providers.travel_time_provider import TravelTimeProvider
from backend.providers.weather_provider import WeatherProvider
from backend.providers.youtube_subscriptions_provider import YouTubeSubscriptionsProvider


def test_weather_normalization():
    provider = WeatherProvider(city="Seattle", latitude=47.6, longitude=-122.3)
    raw = {
        "current": {
            "temperature_2m": 11.1,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 5.5,
            "weather_code": 3,
        }
    }

    out = provider.normalize(raw)

    assert out["city"] == "Seattle"
    assert out["temperature_c"] == 11.1
    assert out["humidity_pct"] == 65
    assert out["wind_kph"] == 5.5
    assert out["condition"] == "Overcast"


def test_time_normalization():
    provider = SystemMetricsProvider(timezones=["UTC", "America/New_York"])
    raw = {
        "utc": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "timezones": ["UTC", "America/New_York"],
    }

    out = provider.normalize(raw)

    assert "utc_iso" in out
    assert len(out["zones"]) == 2
    assert out["zones"][0]["timezone"] == "UTC"


def test_mock_market_normalization_is_stable_shape():
    provider = MockMarketProvider(symbols=["ABC", "XYZ"], seed=1, name="stock_1")
    raw = {
        "quotes": {
            "XYZ": {"price": 10.1, "change_pct": -0.5},
            "ABC": {"price": 20.2, "change_pct": 0.7},
        }
    }

    out = provider.normalize(raw)

    assert [q["symbol"] for q in out["quotes"]] == ["ABC", "XYZ"]
    assert out["quotes"][0]["price"] == 20.2
    assert out["quotes"][0]["open"] is None
    assert provider.name == "stock_1"


def test_real_stock_normalization_is_stable_shape():
    provider = RealStockProvider(symbol="AAPL", name="stock_1")
    raw = {
        "quoteResponse": {
            "result": [
                {
                    "symbol": "AAPL",
                    "shortName": "Apple Inc.",
                    "currency": "USD",
                    "fullExchangeName": "NasdaqGS",
                    "regularMarketPrice": 201.55,
                    "regularMarketChangePercent": 1.23,
                    "regularMarketOpen": 199.1,
                    "regularMarketDayHigh": 202.0,
                    "regularMarketDayLow": 198.7,
                    "regularMarketVolume": 32100000,
                    "marketCap": 3100000000000,
                    "trailingPE": 31.1,
                }
            ]
        }
    }

    out = provider.normalize(raw)
    q = out["quotes"][0]
    assert q["symbol"] == "AAPL"
    assert q["name"] == "Apple Inc."
    assert q["price"] == 201.55
    assert q["source"] == "yahoo_finance"


def test_real_stock_fetch_handles_rate_limit_with_mock(monkeypatch):
    provider = RealStockProvider(symbol="AAPL", name="stock_1", timeout_s=3)

    class FakeResponse:
        status_code = 429
        headers = {"Retry-After": "12"}

        def raise_for_status(self):
            return None

        def json(self):
            return {}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None):
            assert "finance.yahoo.com" in url
            assert params["symbols"] == "AAPL"
            return FakeResponse()

    monkeypatch.setattr("backend.providers.real_stock_provider.httpx.AsyncClient", FakeClient)

    try:
        asyncio.run(provider.fetch())
    except RuntimeError as exc:
        assert "429" in str(exc)
        assert "12s" in str(exc)
    else:
        raise AssertionError("Expected rate-limit RuntimeError")


def test_market_indices_normalization_shape():
    provider = MarketIndicesProvider(symbols=["^GSPC"])
    raw = {
        "quoteResponse": {
            "result": [
                {
                    "symbol": "^GSPC",
                    "shortName": "S&P 500",
                    "regularMarketPrice": 5000.1,
                    "regularMarketChange": 10.2,
                    "regularMarketChangePercent": 0.2,
                }
            ]
        }
    }
    out = provider.normalize(raw)
    assert out["count"] == 1
    assert out["indices"][0]["symbol"] == "^GSPC"


def test_fx_rates_normalization_shape():
    provider = FXRatesProvider(base_currency="USD", symbols=["EUR", "JPY"])
    raw = {"base_code": "USD", "time_last_update_utc": "Sun, 11 Feb 2026 00:00:01 +0000", "rates": {"EUR": 0.91, "JPY": 151.2}}
    out = provider.normalize(raw)
    assert out["base_currency"] == "USD"
    assert len(out["rates"]) == 2
    assert out["rates"][0]["symbol"] == "EUR"


def test_space_weather_normalization_level():
    provider = SpaceWeatherProvider()
    raw = {"series": [{"kp_index": 5.33, "time_tag": "2026-02-11T00:00:00Z"}]}
    out = provider.normalize(raw)
    assert out["level"] == "storm"
    assert out["kp_index"] == 5.33


def test_quote_of_day_normalization_shape():
    provider = QuoteOfDayProvider()
    raw = {"items": [{"q": "Stay hungry, stay foolish.", "a": "Steve Jobs"}]}
    out = provider.normalize(raw)
    assert out["author"] == "Steve Jobs"
    assert "quote" in out


def test_mempool_fees_normalization_shape():
    provider = MempoolFeesProvider()
    raw = {"fastestFee": 22, "halfHourFee": 18, "hourFee": 15, "minimumFee": 6, "economyFee": 8}
    out = provider.normalize(raw)
    assert out["fastest_sat_vb"] == 22
    assert out["source"] == "mempool_space"


def test_nasa_eonet_normalization_shape():
    provider = NASAEONETProvider(limit=2)
    raw = {
        "events": [
            {
                "title": "Wildfire - CA",
                "categories": [{"title": "Wildfires"}],
                "geometry": [{"date": "2026-02-11T00:00:00Z"}],
                "sources": [{"id": "InciWeb"}],
            }
        ]
    }
    out = provider.normalize(raw)
    assert out["count"] == 1
    assert out["events"][0]["category"] == "Wildfires"


def test_solar_xray_normalization_shape():
    provider = SolarXrayProvider()
    raw = {"series": [{"energy": "0.1-0.8nm", "flux": 1.5e-6, "class": "C1.5", "time_tag": "2026-02-11T00:00:00Z"}]}
    out = provider.normalize(raw)
    assert out["flux_class"] == "C1.5"
    assert out["source"] == "noaa_swpc"


def test_crypto_global_normalization_shape():
    provider = CryptoGlobalProvider()
    raw = {
        "data": {
            "active_cryptocurrencies": 12900,
            "markets": 1200,
            "total_market_cap": {"usd": 2500000000000},
            "total_volume": {"usd": 120000000000},
            "market_cap_percentage": {"btc": 51.2, "eth": 16.9},
        }
    }
    out = provider.normalize(raw)
    assert out["markets"] == 1200
    assert out["btc_dominance_pct"] == 51.2


def test_space_launches_normalization_shape():
    provider = SpaceLaunchesProvider(limit=2)
    raw = {
        "results": [
            {
                "name": "Falcon 9 | Starlink",
                "window_start": "2026-02-11T20:00:00Z",
                "status": {"name": "Go"},
                "launch_service_provider": {"name": "SpaceX"},
                "pad": {"location": {"name": "Cape Canaveral"}},
                "mission": {"name": "Starlink Group"},
            }
        ]
    }
    out = provider.normalize(raw)
    assert out["count"] == 1
    assert out["launches"][0]["status"] == "Go"


def test_weather_fetch_uses_external_api_with_mock(monkeypatch):
    provider = WeatherProvider(city="Seattle", latitude=47.6, longitude=-122.3)

    payload = {"current": {"temperature_2m": 10.0}}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None):
            assert "open-meteo.com" in url
            assert "latitude" in params
            return FakeResponse()

    monkeypatch.setattr("backend.providers.weather_provider.httpx.AsyncClient", FakeClient)

    raw = asyncio.run(provider.fetch())
    assert raw == payload


def test_public_status_normalization():
    provider = PublicStatusProvider(services=[])
    raw = {
        "checks": [
            {"name": "A", "ok": True, "latency_ms": 100.0},
            {"name": "B", "ok": False, "latency_ms": None},
            {"name": "C", "ok": True, "latency_ms": 50.0},
        ]
    }

    out = provider.normalize(raw)
    assert out["summary"]["total"] == 3
    assert out["summary"]["up"] == 2
    assert out["summary"]["down"] == 1
    assert out["summary"]["avg_latency_ms"] == 75.0


def test_public_status_fetch_with_mock(monkeypatch):
    provider = PublicStatusProvider(
        services=[
            {"name": "SvcA", "url": "https://a.example", "expect_status": 200},
            {"name": "SvcB", "url": "https://b.example", "expect_status": 204},
        ]
    )

    class FakeResponse:
        def __init__(self, status_code):
            self.status_code = status_code

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, follow_redirects=True):
            if "a.example" in url:
                return FakeResponse(200)
            return FakeResponse(500)

    monkeypatch.setattr("backend.providers.public_status_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())

    assert len(raw["checks"]) == 2
    assert raw["checks"][0]["ok"] is True
    assert raw["checks"][1]["ok"] is False


def test_heartbeat_normalization_shape():
    provider = HeartbeatProvider()
    raw = asyncio.run(provider.fetch())
    out = provider.normalize(raw)
    assert out["heartbeat"] == "alive"
    assert isinstance(out["uptime_seconds"], float)
    assert out["utc_now"] is not None


def test_usa_severe_weather_normalization_ranks_worst():
    provider = USASevereWeatherProvider(cities=[], top_n=2)
    raw = {
        "cities": [
            {
                "city": "Calmville",
                "state": "CA",
                "weather_code": 1,
                "wind_speed_10m": 5,
                "precipitation": 0,
                "temperature_2m": 22,
            },
            {
                "city": "Storm City",
                "state": "TX",
                "weather_code": 95,
                "wind_speed_10m": 60,
                "precipitation": 12,
                "temperature_2m": 30,
            },
            {
                "city": "Wind Town",
                "state": "OK",
                "weather_code": 3,
                "wind_speed_10m": 41,
                "precipitation": 2,
                "temperature_2m": 20,
            },
        ]
    }

    out = provider.normalize(raw)
    assert out["national"]["monitored_cities"] == 3
    assert out["worst"][0]["city"] == "Storm City"
    assert len(out["worst"]) == 2
    assert out["national"]["severity_level"] in {"elevated", "severe"}


def test_usa_severe_weather_fetch_with_mock(monkeypatch):
    provider = USASevereWeatherProvider(
        cities=[{"city": "Seattle", "state": "WA", "latitude": 47.6, "longitude": -122.3}]
    )

    payload = {
        "current": {
            "temperature_2m": 7,
            "wind_speed_10m": 15,
            "precipitation": 0,
            "weather_code": 1,
        }
    }

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None):
            assert "open-meteo.com" in url
            return FakeResponse()

    monkeypatch.setattr("backend.providers.usa_severe_weather_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())

    assert raw["cities"][0]["city"] == "Seattle"
    assert raw["cities"][0]["weather_code"] == 1


def test_youtube_normalization_sorts_latest_and_limits():
    provider = YouTubeSubscriptionsProvider(channel_ids=["UC1", "UC2"], max_videos=2)
    raw = {
        "feeds": [
            {
                "channel_id": "UC1",
                "entries": [
                    {
                        "video_id": "a1",
                        "title": "Older",
                        "channel_id": "UC1",
                        "channel_title": "C1",
                        "published_at": "2026-01-01T10:00:00+00:00",
                        "url": "https://youtube.com/watch?v=a1",
                    }
                ],
            },
            {
                "channel_id": "UC2",
                "entries": [
                    {
                        "video_id": "b1",
                        "title": "Newest",
                        "channel_id": "UC2",
                        "channel_title": "C2",
                        "published_at": "2026-01-02T10:00:00+00:00",
                        "url": "https://youtube.com/watch?v=b1",
                    },
                    {
                        "video_id": "b2",
                        "title": "Middle",
                        "channel_id": "UC2",
                        "channel_title": "C2",
                        "published_at": "2026-01-01T15:00:00+00:00",
                        "url": "https://youtube.com/watch?v=b2",
                    },
                ],
            },
        ],
        "errors": [],
    }

    out = provider.normalize(raw)
    assert out["summary"]["videos"] == 2
    assert out["videos"][0]["video_id"] == "b1"
    assert out["videos"][1]["video_id"] == "b2"


def test_youtube_fetch_with_mock(monkeypatch):
    provider = YouTubeSubscriptionsProvider(channel_ids=["UC1234567890123456789012"], max_videos=5)
    xml_text = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<feed xmlns=\"http://www.w3.org/2005/Atom\" xmlns:yt=\"http://www.youtube.com/xml/schemas/2015\">
  <title>Channel Feed</title>
  <entry>
    <yt:videoId>vid123</yt:videoId>
    <title>Test Video</title>
    <published>2026-01-01T10:00:00+00:00</published>
    <author><name>Test Channel</name></author>
    <link rel=\"alternate\" href=\"https://www.youtube.com/watch?v=vid123\"/>
  </entry>
</feed>
"""

    class FakeResponse:
        def raise_for_status(self):
            return None

        @property
        def text(self):
            return xml_text

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None, follow_redirects=True, headers=None):
            assert "youtube.com/feeds/videos.xml" in url
            return FakeResponse()

    monkeypatch.setattr("backend.providers.youtube_subscriptions_provider.httpx.AsyncClient", FakeClient)

    raw = asyncio.run(provider.fetch())
    assert len(raw["feeds"]) == 1
    assert raw["feeds"][0]["entries"][0]["video_id"] == "vid123"


def test_youtube_resolves_handle_with_mock(monkeypatch):
    provider = YouTubeSubscriptionsProvider(channel_ids=["@mychannel"], max_videos=5)
    channel_html = '<html><script>var x={"channelId":"UC_HANDLE_1234567890123456"}</script></html>'
    oembed_payload = {"author_url": "https://www.youtube.com/channel/UC_HANDLE_1234567890123456"}
    xml_text = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<feed xmlns=\"http://www.w3.org/2005/Atom\" xmlns:yt=\"http://www.youtube.com/xml/schemas/2015\">
  <title>Channel Feed</title>
  <entry>
    <yt:videoId>vid999</yt:videoId>
    <title>Handle Video</title>
    <published>2026-01-01T10:00:00+00:00</published>
    <author><name>Handle Channel</name></author>
    <link rel=\"alternate\" href=\"https://www.youtube.com/watch?v=vid999\"/>
  </entry>
</feed>
"""

    class FakeResponse:
        def __init__(self, text=None, json_payload=None, status_code=200):
            self._text = text
            self._json_payload = json_payload
            self.status_code = status_code

        def raise_for_status(self):
            return None

        @property
        def text(self):
            return self._text

        def json(self):
            return self._json_payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None, follow_redirects=True, headers=None):
            if "youtube.com/oembed" in url:
                return FakeResponse(json_payload=oembed_payload)
            if "feeds/videos.xml" in url:
                return FakeResponse(xml_text)
            return FakeResponse(channel_html)

    monkeypatch.setattr("backend.providers.youtube_subscriptions_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())

    assert raw["resolved_channels"] == 1
    assert raw["feeds"][0]["entries"][0]["video_id"] == "vid999"


def test_travel_time_normalization_orders_fastest():
    provider = TravelTimeProvider(origin={"name": "Home", "latitude": 1, "longitude": 1}, destinations=[])
    raw = {
        "origin": {"name": "Home", "latitude": 1, "longitude": 1},
        "routes": [
            {"name": "Office", "minutes": 35, "distance_km": 20.0, "status": "ok", "error": None},
            {"name": "Gym", "minutes": 12, "distance_km": 6.0, "status": "ok", "error": None},
            {"name": "Unknown", "minutes": None, "distance_km": None, "status": "error", "error": "No route"},
        ],
    }
    out = provider.normalize(raw)
    assert out["summary"]["destinations"] == 3
    assert out["summary"]["reachable"] == 2
    assert out["summary"]["fastest_minutes"] == 12
    assert out["routes"][0]["name"] == "Gym"


def test_travel_time_fetch_with_mock(monkeypatch):
    provider = TravelTimeProvider(
        origin={"name": "Home", "latitude": 47.6, "longitude": -122.3},
        destinations=[{"name": "Office", "latitude": 47.7, "longitude": -122.4}],
    )
    payload = {"routes": [{"duration": 900, "distance": 12000}]}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None):
            assert "router.project-osrm.org" in url
            return FakeResponse()

    monkeypatch.setattr("backend.providers.travel_time_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())
    assert raw["routes"][0]["name"] == "Office"
    assert raw["routes"][0]["minutes"] == 15


def test_travel_time_fetch_with_address_geocoding(monkeypatch):
    provider = TravelTimeProvider(
        origin={"name": "Home", "address": "Spokane, WA"},
        destinations=[{"name": "Airport", "address": "Spokane International Airport"}],
    )

    class FakeResponse:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self._payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None, headers=None):
            if "nominatim.openstreetmap.org/search" in url:
                q = params.get("q", "")
                if "Airport" in q:
                    return FakeResponse([{"lat": "47.6199", "lon": "-117.5338"}])
                return FakeResponse([{"lat": "47.6588", "lon": "-117.4260"}])
            assert "router.project-osrm.org" in url
            return FakeResponse({"routes": [{"duration": 1200, "distance": 18000}]})

    monkeypatch.setattr("backend.providers.travel_time_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())
    assert raw["routes"][0]["name"] == "Airport"
    assert raw["routes"][0]["minutes"] == 20


def test_travel_time_fetch_handles_geocode_failure_without_crashing(monkeypatch):
    provider = TravelTimeProvider(
        origin={"name": "Home", "address": "Bad Origin"},
        destinations=[{"name": "Office", "address": "Bad Destination"}],
    )

    class FakeResponse:
        status_code = 429

        def raise_for_status(self):
            request = httpx.Request("GET", "https://nominatim.openstreetmap.org/search")
            response = httpx.Response(429, request=request)
            raise httpx.HTTPStatusError("rate limited", request=request, response=response)

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params=None, headers=None):
            return FakeResponse()

    monkeypatch.setattr("backend.providers.travel_time_provider.httpx.AsyncClient", FakeClient)
    raw = asyncio.run(provider.fetch())
    assert raw["routes"][0]["status"] == "error"
    assert "Origin" in raw["routes"][0]["error"]
