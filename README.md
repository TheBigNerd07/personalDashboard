# Real-Time Data Monitor

A lightweight operations-style dashboard that polls multiple live data sources, normalizes them into a consistent schema, and displays their status in near real time.

## Stack

- Backend: Python 3.9+, FastAPI, asyncio
- Frontend: Vanilla HTML/CSS/JS
- Tests: pytest

## Implemented Data Sources

- `weather`: live current conditions from Open-Meteo (city by lat/lon)
- `system_metrics`: UTC/local + multiple timezone clocks
- `stock_1`, `stock_2`, `stock_3`: independent configurable live stock modules (Yahoo Finance quote feed) with chart history and rate-limit handling
- `public_status`: live checks against configured public service endpoints
- `heartbeat`: local runtime heartbeat and uptime signal
- `usa_severe_weather`: ranks worst current weather across configured U.S. cities
- `youtube_subscriptions`: latest videos from configured YouTube channel IDs
- `travel_time`: driving ETA from one origin to multiple destinations
- `crypto_price`: live Coinbase spot crypto ticker
- `hn_trends`: Hacker News top story monitor
- `earthquakes`: USGS earthquake feed (last hour)
- `sun_times`: sunrise/sunset/day-length tracker
- `air_quality`: Open-Meteo AQI and particulates
- `iss_position`: live ISS latitude/longitude
- `network_dns`: DNS health checks for key hosts
- `market_indices`: live S&P/Nasdaq/Dow/VIX index monitor
- `fx_rates`: live FX rates for configured base currency
- `space_weather`: NOAA planetary K-index status
- `quote_of_day`: daily quote stream
- `mempool_fees`: live Bitcoin mempool fee recommendations
- `nasa_events`: open natural event feed from NASA EONET
- `solar_xray`: NOAA GOES solar X-ray flux monitor
- `crypto_global`: global crypto market cap and dominance metrics
- `space_launches`: upcoming launch schedule from The Space Devs

Each provider runs independently with its own polling interval, cache TTL, and failure handling.

## Project Structure

- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/providers/weather_provider.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/providers/system_metrics_provider.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/providers/mock_market_provider.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/providers/real_stock_provider.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/scheduler.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/api.py`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/frontend/index.html`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/frontend/styles.css`
- `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/frontend/app.js`

## Normalized Internal Format

Each provider emits:

```json
{
  "source": "weather",
  "status": "ok|stale|error",
  "data": {},
  "fetched_at": "ISO8601",
  "error": null
}
```

Scheduler snapshot includes:

```json
{
  "paused": false,
  "global_refresh_rate": 1.0,
  "generated_at": "ISO8601",
  "source_count": 3,
  "sources": [
    {
      "source": "weather",
      "status": "ok",
      "source_paused": false,
      "data": {},
      "fetched_at": "ISO8601",
      "error": null,
      "poll_interval": 10,
      "history": []
    }
  ]
}
```

## Configuration

Edit `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/config.json`:

```json
{
  "appearance_mode": "light",
  "theme": {
    "bg": "#F2F2F7",
    "accent": "#0A84FF",
    "error": "#D72D20"
  },
  "global_refresh_rate": 1.0,
  "history_size": 20,
  "providers": {
    "weather": { "enabled": true, "poll_interval": 10, "cache_ttl": 4 },
    "system_metrics": { "enabled": true, "poll_interval": 1, "cache_ttl": 1 },
    "stock_1": { "enabled": true, "symbol": "AAPL", "poll_interval": 2, "cache_ttl": 2, "timeout_s": 6 },
    "stock_2": { "enabled": true, "symbol": "MSFT", "poll_interval": 2, "cache_ttl": 2, "timeout_s": 6 },
    "stock_3": { "enabled": true, "symbol": "NVDA", "poll_interval": 2, "cache_ttl": 2, "timeout_s": 6 }
  }
}
```

Set `unit_system` to `imperial` or `metric` to control UI units (temperature, wind, and travel distance).
Set `appearance_mode` to `light` or `dark` (or use the toolbar toggle).
Set `theme` hex values in Settings to live-customize dashboard colors.

For `youtube_subscriptions`, add one channel per line in Settings (channel ID, `@handle`, or channel URL), or set them in `config.json` under `providers.youtube_subscriptions.channel_ids`. This app currently uses public RSS feeds and does not authenticate directly to your Google account.

`travel_time` uses free address geocoding via OpenStreetMap Nominatim plus free OSRM routing (`router.project-osrm.org`) for driving ETA estimates. You can enter addresses directly in Settings.

## Run Locally

1. Create and activate a virtualenv.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start app:

```bash
uvicorn backend.api:app --reload
```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Dashboard Features

- Single-page card-based layout
- Current values + timestamps + status indicator
- Auto-refresh without full reload
- Global refresh-rate control
- Global pause/resume
- Per-source pause/resume
- Manual refresh-now (all sources or per source)
- Search + status filter (`all/ok/stale/error`)
- Health summary bar (counts by status)
- Snapshot export to JSON
- Settings menu with full JSON config editor
- Settings persist to `config.json` and apply live without restarting the app
- In-memory history per source with compact trend hints
- USA severe weather ranking card (worst locations + national severity level)
- Mixed card sizing: full and half-width modules (two half modules fit one full slot)
- Wallboard mode
- Light/Dark mode toggle
- Per-source error messages

## API Endpoints

- `GET /api/settings`
- `POST /api/settings`
- `GET /api/snapshot`
- `POST /api/pause`
- `POST /api/resume`
- `POST /api/refresh-rate`
- `POST /api/refresh-now`
- `POST /api/source/{source}/pause`
- `POST /api/source/{source}/resume`

## Testing

Run:

```bash
pytest -q
```

Covered:

- config save/load roundtrip
- provider normalization logic
- mocked weather external API fetch
- mocked public status external fetch
- mocked YouTube feed fetch
- scheduler polling behavior
- scheduler pause/resume behavior
- source-level controls + manual refresh + history

## Add a New Provider

1. Create a provider class in `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/providers/` implementing `BaseProvider`:
   - `async fetch(self) -> dict`
   - `normalize(self, raw: dict) -> dict`
2. Register it in `build_providers()` in `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/backend/api.py`.
3. Add config options under `providers.<name>` in `/Users/bignerd/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/personalDashboard/config.json`.
4. Add tests for normalization and failure cases.

## Reliability Notes

- Provider failures do not crash scheduler loops.
- Each provider runs in its own async task.
- Stale status is computed from cache TTL.
- Stock modules handle upstream HTTP 429 rate limits with retry-after cooldown windows.
- Scheduler supports global and source-level controls at runtime.
- Per-source history is bounded in-memory (`history_size`) to avoid unbounded growth.
