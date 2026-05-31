from __future__ import annotations

import asyncio

from app.config import reset_settings_cache
from app.models import Project, ServiceCard, Task
from app.services.briefing import create_daily_briefing, fallback_briefing, build_dashboard_context
from app.services.llm import LLMUnavailable
from app.services.weather import WeatherSnapshot


def test_fallback_briefing_contains_required_sections(db_session):
    db_session.add(Task(title="Add current school deadlines", category="school", priority="high", status="active"))
    db_session.add(Project(name="Stride Shots Workflow", category="Stride Shots", next_action="Choose next event workflow step"))
    db_session.add(ServiceCard(name="Portainer", last_status="down"))
    db_session.commit()

    context = build_dashboard_context(db_session, WeatherSnapshot(available=False))
    markdown = fallback_briefing(context)

    assert "## Focus" in markdown
    assert "## Weather" in markdown
    assert "## Deadlines" in markdown
    assert "## Projects" in markdown
    assert "## Homelab" in markdown
    assert "## Stride Shots" in markdown
    assert "## Watch" in markdown


def test_llm_unavailable_uses_basic_fallback(db_session, monkeypatch):
    class FailingLLM:
        async def generate_daily_briefing(self, dashboard_context):
            raise LLMUnavailable("offline")

    monkeypatch.setenv("LLM_ENABLED", "true")
    reset_settings_cache()
    db_session.add(Task(title="Configure LM Studio", category="homelab", priority="normal", status="active"))
    db_session.commit()

    result = asyncio.run(
        create_daily_briefing(
            db_session,
            weather=WeatherSnapshot(available=False),
            use_ai=True,
            llm_client=FailingLLM(),
        )
    )

    assert result.mode == "basic"
    assert result.notice == "Local AI unavailable - using basic briefing."
    assert "## Watch" in result.markdown
    assert "Configure LM Studio" not in result.markdown
    reset_settings_cache()
