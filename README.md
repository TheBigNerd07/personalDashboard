# Command Center

Command Center is a Docker-first personal productivity dashboard for Logan. It runs as a lightweight FastAPI app with SQLite storage and server-rendered pages, so it is practical for a Raspberry Pi, Tailscale, and a small homelab.

## Features

- Today / Focus panel with editable daily focus, top tasks, and upcoming deadlines
- Task, project, quick note, and homelab service management
- Optional service health checks that fail safely when a service is unreachable
- Optional Post Falls, Idaho weather via Open-Meteo
- Daily briefing with deterministic fallback logic
- Optional LM Studio integration through an OpenAI-compatible local API
- Optional password protection with signed session cookies
- REST API for tasks, projects, notes, services, settings, health, and briefing regeneration

## Screenshots

Add screenshots here after the first deployment.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Open [http://localhost:8080](http://localhost:8080).

The local default database path is `./data/command_center.db`. Tables are created automatically on startup. Seed data is added only when the database is empty.

## Docker Compose

```bash
cp .env.example .env
docker compose up -d --build
```

Open [http://localhost:8080](http://localhost:8080).

The compose file persists data with:

```yaml
./data:/app/data
```

It also includes:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

That is useful only when LM Studio runs on the Docker host. Logan's recommended setup is to use the PC's LAN IP, Tailscale IP, or MagicDNS hostname instead.

## Raspberry Pi Deployment

1. Install Debian or Raspberry Pi OS Lite.
2. Install Docker and Docker Compose.
3. Clone this repository onto the Pi.
4. Copy `.env.example` to `.env`.
5. Set `SECRET_KEY` to a long random value.
6. Run `docker compose up -d --build`.
7. Back up the `./data` directory regularly.

The app uses Python, FastAPI, SQLite, and plain server-rendered HTML. It does not require Kubernetes, a Node build pipeline, cloud services, or paid APIs.

## Nginx Proxy Manager

1. Create a new proxy host.
2. Set the forward hostname/IP to the Command Center host.
3. Set the forward port to `8080`.
4. Enable Websockets if you use them later.
5. Request an SSL certificate if exposing through a trusted domain.
6. Prefer Tailscale-only access unless you intentionally expose it publicly.

## Cloudflare Tunnel

At a high level:

1. Install `cloudflared` on the host or run it as a container.
2. Create a tunnel in Cloudflare Zero Trust.
3. Point a public hostname to `http://command-center:8080` or `http://<host-ip>:8080`.
4. Add Cloudflare Access or keep Command Center's `APP_PASSWORD` enabled if the dashboard is reachable outside your private network.

## Optional Password Protection

Authentication is disabled when `APP_PASSWORD` is empty:

```env
APP_PASSWORD=
```

To enable it:

```env
APP_PASSWORD=choose-a-password
SECRET_KEY=replace-with-a-long-random-string
```

Restart the container after changing `.env`.

## LM Studio Setup

LM Studio is optional. Command Center works normally when Logan's PC is off, asleep, or unreachable. If the local AI call fails, the dashboard logs a warning, shows a small notice, and uses the deterministic basic briefing.

Recommended remote setup:

1. On the PC running LM Studio:
   - Open LM Studio.
   - Download a small chat or instruct model.
   - Start the Local Server.
   - Enable access from other devices on the LAN if LM Studio provides that setting.
   - Confirm the server listens on port `1234`.
   - Check that the PC firewall allows inbound connections to port `1234` from the Raspberry Pi or Tailscale network.
2. On the Command Center host, set:

```env
LLM_ENABLED=true
LLM_BASE_URL=http://<PC_IP_OR_TAILSCALE_IP>:1234/v1
LLM_MODEL=<model name shown in LM Studio>
LLM_TIMEOUT_SECONDS=8
```

3. Test from the Command Center host:

```bash
curl http://<PC_IP_OR_TAILSCALE_IP>:1234/v1/models
```

4. If running Command Center outside Docker on the same machine as LM Studio, use:

```env
LLM_BASE_URL=http://localhost:1234/v1
```

5. If LM Studio runs on the Docker host, this can work:

```env
LLM_BASE_URL=http://host.docker.internal:1234/v1
```

For Logan's setup, prefer the PC's Tailscale IP, LAN IP, or MagicDNS hostname:

```env
LLM_BASE_URL=http://100.x.y.z:1234/v1
LLM_BASE_URL=http://192.168.1.50:1234/v1
LLM_BASE_URL=http://logan-pc.tailnet-name.ts.net:1234/v1
```

If the curl test fails:

- Make sure the LM Studio server is running.
- Make sure the PC is awake.
- Check firewall rules.
- Try the Tailscale IP instead of the LAN IP.
- Confirm both machines are on the same network or Tailnet.

Expected behavior:

- If `LLM_ENABLED=false`, Command Center never calls LM Studio.
- If the PC is off, Command Center still works.
- AI briefing falls back to basic mode.
- No dashboard features should break.

## Weather

Weather is optional and uses Open-Meteo. Defaults are set for Post Falls, Idaho:

```env
WEATHER_ENABLED=true
WEATHER_LATITUDE=47.712
WEATHER_LONGITUDE=-116.948
WEATHER_TIMEZONE=America/Los_Angeles
```

If Open-Meteo is unavailable, the weather card displays an unavailable message and the rest of the dashboard continues to load.

## API

- `GET /health`
- `GET /`
- `GET /briefing`
- `POST /briefing/regenerate`
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `PATCH /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
- `POST /api/tasks/{id}/complete`
- `GET /api/projects`
- `POST /api/projects`
- `PATCH /api/projects/{id}`
- `DELETE /api/projects/{id}`
- `GET /api/notes`
- `POST /api/notes`
- `PATCH /api/notes/{id}`
- `DELETE /api/notes/{id}`
- `GET /api/services`
- `POST /api/services`
- `PATCH /api/services/{id}`
- `DELETE /api/services/{id}`
- `POST /api/services/check`
- `GET /api/settings`
- `PATCH /api/settings`

## Tests

```bash
pytest
```

The tests do not require LM Studio, internet access, Discord, or paid external APIs.

## Backups

The SQLite database lives in `./data`. To back it up:

```bash
mkdir -p backups
cp data/command_center.db backups/command_center-$(date +%Y%m%d-%H%M%S).db
```

For a running container, you can stop briefly before copying:

```bash
docker compose stop command-center
cp data/command_center.db backups/
docker compose up -d
```

Do not delete `./data` unless you intentionally want to reset the dashboard.

