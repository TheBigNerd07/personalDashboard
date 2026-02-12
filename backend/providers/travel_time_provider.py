from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Tuple

import httpx

from backend.providers.base import BaseProvider


class TravelTimeProvider(BaseProvider):
    name = "travel_time"

    def __init__(
        self,
        origin: Dict[str, Any],
        destinations: List[Dict[str, Any]],
        enabled: bool = True,
        poll_interval: float = 45.0,
        cache_ttl: float = 20.0,
        timeout_s: float = 8.0,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.origin = origin
        self.destinations = destinations
        self.timeout_s = timeout_s
        self._geocode_cache: Dict[str, Tuple[float, float]] = {}

    @staticmethod
    def _http_error_message(exc: Exception, context: str) -> str:
        if isinstance(exc, httpx.HTTPStatusError):
            code = exc.response.status_code
            if code == 429:
                return f"{context} rate limited (HTTP 429)"
            if code == 509:
                return f"{context} bandwidth limit reached (HTTP 509)"
            return f"{context} failed (HTTP {code})"
        if isinstance(exc, httpx.RequestError):
            return f"{context} network error"
        return f"{context} failed"

    async def _geocode_address(self, client: httpx.AsyncClient, address: str) -> Tuple[float, float] | None:
        key = (address or "").strip()
        if not key:
            return None
        if key in self._geocode_cache:
            return self._geocode_cache[key]

        try:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": key, "format": "jsonv2", "limit": 1},
                headers={"User-Agent": "personalDashboard/1.0"},
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return None

        try:
            if not payload:
                return None
            lat = float(payload[0]["lat"])
            lon = float(payload[0]["lon"])
            self._geocode_cache[key] = (lat, lon)
            return lat, lon
        except Exception:
            return None

    async def _resolve_point(self, client: httpx.AsyncClient, point: Dict[str, Any]) -> Tuple[float, float] | None:
        lat = point.get("latitude")
        lon = point.get("longitude")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            return float(lat), float(lon)

        address = point.get("address")
        if isinstance(address, str) and address.strip():
            return await self._geocode_address(client, address.strip())

        return None

    async def _route_to_destination(
        self,
        client: httpx.AsyncClient,
        destination: Dict[str, Any],
        origin_coords: Tuple[float, float] | None,
        origin_error: str | None = None,
    ) -> Dict[str, Any]:
        destination_name = destination.get("name") or destination.get("address") or "Unknown"
        if origin_coords is None:
            return {
                "name": destination_name,
                "minutes": None,
                "distance_km": None,
                "status": "error",
                "error": origin_error or "Origin could not be resolved",
            }

        dest_coords = await self._resolve_point(client, destination)

        if dest_coords is None:
            return {
                "name": destination_name,
                "minutes": None,
                "distance_km": None,
                "status": "error",
                "error": "Destination could not be resolved",
            }

        origin_lat, origin_lon = origin_coords
        dest_lat, dest_lon = dest_coords

        coord_str = f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
        url = f"https://router.project-osrm.org/route/v1/driving/{coord_str}"
        params = {"overview": "false", "alternatives": "false", "steps": "false"}

        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
            routes = payload.get("routes", [])
            if not routes:
                raise ValueError("No route found")

            route = routes[0]
            duration_s = float(route.get("duration", 0))
            distance_m = float(route.get("distance", 0))
            return {
                "name": destination_name,
                "minutes": round(duration_s / 60.0),
                "distance_km": round(distance_m / 1000.0, 1),
                "status": "ok",
                "error": None,
            }
        except Exception as exc:
            return {
                "name": destination_name,
                "minutes": None,
                "distance_km": None,
                "status": "error",
                "error": self._http_error_message(exc, "Routing"),
            }

    async def fetch(self) -> Dict[str, Any]:
        if not self.destinations:
            return {"origin": self.origin, "routes": []}

        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            origin_coords = await self._resolve_point(client, self.origin)
            origin_error = None if origin_coords is not None else "Origin could not be resolved"
            routes = await asyncio.gather(
                *(
                    self._route_to_destination(
                        client=client,
                        destination=destination,
                        origin_coords=origin_coords,
                        origin_error=origin_error,
                    )
                    for destination in self.destinations
                )
            )

        return {"origin": self.origin, "routes": routes}

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        routes = raw.get("routes", [])
        ok_routes = [r for r in routes if r.get("status") == "ok" and isinstance(r.get("minutes"), (int, float))]
        ok_routes_sorted = sorted(ok_routes, key=lambda x: x.get("minutes", 999999))

        return {
            "origin": raw.get("origin", {}),
            "summary": {
                "destinations": len(routes),
                "reachable": len(ok_routes),
                "fastest_minutes": ok_routes_sorted[0]["minutes"] if ok_routes_sorted else None,
            },
            "routes": sorted(routes, key=lambda x: (x.get("minutes") is None, x.get("minutes") or 999999)),
        }
