from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database import get_session, set_setting
from app.services.briefing import create_daily_briefing
from app.services.weather import fetch_weather

router = APIRouter(tags=["briefing"])


@router.get("/briefing")
async def get_briefing(session: Session = Depends(get_session)) -> dict:
    weather = await fetch_weather()
    briefing = await create_daily_briefing(session, weather=weather, use_ai=False)
    return {
        "mode": briefing.mode,
        "markdown": briefing.markdown,
        "notice": briefing.notice,
        "generated_at": briefing.generated_at.isoformat(),
        "last_ai_markdown": briefing.last_ai_markdown,
        "last_ai_generated_at": briefing.last_ai_generated_at,
    }


@router.post("/briefing/regenerate")
async def regenerate_briefing(request: Request, session: Session = Depends(get_session)):
    weather = await fetch_weather()
    briefing = await create_daily_briefing(session, weather=weather, use_ai=True)
    set_setting(session, "latest_ai_notice", briefing.notice or "")
    accept = request.headers.get("accept", "")
    content_type = request.headers.get("content-type", "")
    if "text/html" in accept or "application/x-www-form-urlencoded" in content_type:
        return RedirectResponse(url="/#briefing", status_code=303)
    return {
        "mode": briefing.mode,
        "markdown": briefing.markdown,
        "notice": briefing.notice,
        "generated_at": briefing.generated_at.isoformat(),
        "last_ai_markdown": briefing.last_ai_markdown,
        "last_ai_generated_at": briefing.last_ai_generated_at,
    }
