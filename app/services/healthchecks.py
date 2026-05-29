from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import httpx
from sqlmodel import Session

from app.models import ServiceCard, utcnow

logger = logging.getLogger(__name__)


@dataclass
class HealthcheckResult:
    status: str
    error: Optional[str] = None


async def check_health_url(
    url: Optional[str],
    *,
    timeout_seconds: float = 4.0,
    client: Optional[httpx.AsyncClient] = None,
) -> HealthcheckResult:
    if not url:
        return HealthcheckResult(status="unknown")

    async def _request(active_client: httpx.AsyncClient) -> HealthcheckResult:
        response = await active_client.get(url)
        if 200 <= response.status_code < 400:
            return HealthcheckResult(status="up")
        return HealthcheckResult(status="down", error=f"HTTP {response.status_code}")

    try:
        if client is not None:
            return await _request(client)
        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as active_client:
            return await _request(active_client)
    except httpx.HTTPError as exc:
        logger.warning("Service health check failed for %s: %s", url, exc)
        return HealthcheckResult(status="down", error=str(exc))


async def update_service_health(session: Session, service: ServiceCard) -> ServiceCard:
    result = await check_health_url(service.healthcheck_url)
    service.last_status = result.status
    service.last_checked_at = utcnow()
    session.add(service)
    session.commit()
    session.refresh(service)
    return service
