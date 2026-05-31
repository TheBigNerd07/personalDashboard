from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Optional

from sqlmodel import Session, select

from app.config import get_settings
from app.database import get_setting, set_setting
from app.models import Note, Project, ServiceCard, Task
from app.services.llm import LLMUnavailable, LMStudioClient
from app.services.weather import WeatherSnapshot

logger = logging.getLogger(__name__)

PRIORITY_ORDER = {"urgent": 0, "high": 1, "normal": 2, "low": 3}


@dataclass
class BriefingResult:
    markdown: str
    mode: str
    generated_at: datetime
    notice: Optional[str] = None
    last_ai_markdown: Optional[str] = None
    last_ai_generated_at: Optional[str] = None


def _task_sort_key(task: Task) -> tuple[int, date, datetime]:
    return (
        PRIORITY_ORDER.get(task.priority, 4),
        task.due_date or date.max,
        task.created_at,
    )


def _task_dict(task: Task) -> dict[str, Any]:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "priority": task.priority,
        "status": task.status,
        "due_date": task.due_date.isoformat() if task.due_date else None,
    }


def _project_dict(project: Project) -> dict[str, Any]:
    return {
        "id": project.id,
        "name": project.name,
        "category": project.category,
        "status": project.status,
        "next_action": project.next_action,
        "link": project.link,
    }


def _service_dict(service: ServiceCard) -> dict[str, Any]:
    return {
        "id": service.id,
        "name": service.name,
        "category": service.category,
        "url": service.url,
        "last_status": service.last_status,
        "last_checked_at": service.last_checked_at.isoformat() if service.last_checked_at else None,
    }


def _note_dict(note: Note) -> dict[str, Any]:
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "tags": note.tags,
        "updated_at": note.updated_at.isoformat(),
    }


def build_dashboard_context(session: Session, weather: Optional[WeatherSnapshot] = None) -> dict[str, Any]:
    today = date.today()
    tasks = session.exec(select(Task).where(Task.status != "archived")).all()
    active_tasks = [task for task in tasks if task.status in {"inbox", "active"}]
    top_tasks = sorted(active_tasks, key=_task_sort_key)[:3]
    upcoming_deadlines = sorted(
        [
            task
            for task in active_tasks
            if task.due_date is not None and today <= task.due_date <= today + timedelta(days=14)
        ],
        key=_task_sort_key,
    )
    projects = session.exec(select(Project).where(Project.status.in_(["active", "paused"]))).all()
    services = session.exec(select(ServiceCard).order_by(ServiceCard.sort_order, ServiceCard.name)).all()
    notes = session.exec(select(Note).order_by(Note.updated_at.desc())).all()[:5]
    active_project_dicts = [_project_dict(project) for project in projects if project.status == "active"]

    return {
        "date": today.isoformat(),
        "todays_focus": get_setting(session, "todays_focus", "Choose one important task and move it forward."),
        "attention_signals": [_task_dict(task) for task in top_tasks if task.priority in {"urgent", "high"}],
        "upcoming_deadlines": [_task_dict(task) for task in upcoming_deadlines],
        "active_projects": active_project_dicts,
        "paused_projects": [_project_dict(project) for project in projects if project.status == "paused"],
        "homelab_projects": [project for project in active_project_dicts if project["category"].lower() == "homelab"],
        "stride_shots_projects": [project for project in active_project_dicts if project["category"].lower() == "stride shots"],
        "homelab_attention_items": [_service_dict(service) for service in services if service.last_status == "down"],
        "recent_notes": [_note_dict(note) for note in notes],
        "weather": weather.__dict__ if weather else None,
    }


def _line_items(items: list[dict[str, Any]], title_key: str = "title", empty: str = "None listed.") -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item.get(title_key) or item.get('name')}: {item.get('next_action') or item.get('priority') or item.get('status') or ''}".rstrip(": ") for item in items)


def fallback_briefing(context: dict[str, Any]) -> str:
    weather = context.get("weather") or {}
    weather_line = "Weather unavailable."
    if weather.get("available"):
        parts = [f"{weather.get('temperature')}F", weather.get("condition")]
        if weather.get("high") is not None and weather.get("low") is not None:
            parts.append(f"high {weather.get('high')}F / low {weather.get('low')}F")
        if weather.get("precipitation_chance") is not None:
            parts.append(f"{weather.get('precipitation_chance')}% precip")
        weather_line = ", ".join(str(part) for part in parts if part)

    return "\n\n".join(
        [
            "## Focus\n" + context["todays_focus"],
            "## Weather\n" + weather_line,
            "## Deadlines\n" + _line_items(context["upcoming_deadlines"], empty="No deadlines in the next 14 days."),
            "## Projects\n" + _line_items(context["active_projects"], title_key="name", empty="No active projects."),
            "## Homelab\n"
            + _line_items(
                context["homelab_attention_items"] or context["homelab_projects"],
                title_key="name",
                empty="No homelab alerts.",
            ),
            "## Stride Shots\n"
            + _line_items(
                context["stride_shots_projects"],
                title_key="name",
                empty="No Stride Shots project signal configured.",
            ),
            "## Watch\nKeep an eye on service health, dated school items, and any Stride Shots project with an upcoming delivery window.",
        ]
    )


async def create_daily_briefing(
    session: Session,
    *,
    weather: Optional[WeatherSnapshot] = None,
    use_ai: bool = False,
    llm_client: Optional[LMStudioClient] = None,
) -> BriefingResult:
    context = build_dashboard_context(session, weather)
    generated_at = datetime.utcnow()
    last_ai_markdown = get_setting(session, "latest_ai_briefing", "")
    last_ai_generated_at = get_setting(session, "latest_ai_briefing_at", "")

    if not use_ai:
        return BriefingResult(
            markdown=fallback_briefing(context),
            mode="basic",
            generated_at=generated_at,
            last_ai_markdown=last_ai_markdown or None,
            last_ai_generated_at=last_ai_generated_at or None,
        )

    settings = get_settings()
    if not settings.llm_enabled:
        return BriefingResult(
            markdown=fallback_briefing(context),
            mode="basic",
            generated_at=generated_at,
            notice="Local AI disabled - using basic briefing.",
            last_ai_markdown=last_ai_markdown or None,
            last_ai_generated_at=last_ai_generated_at or None,
        )

    try:
        client = llm_client or LMStudioClient(settings)
        markdown = await client.generate_daily_briefing(context)
        ai_generated_at = generated_at.isoformat(timespec="seconds") + "Z"
        set_setting(session, "latest_ai_briefing", markdown)
        set_setting(session, "latest_ai_briefing_at", ai_generated_at)
        return BriefingResult(
            markdown=markdown,
            mode="ai",
            generated_at=generated_at,
            last_ai_markdown=markdown,
            last_ai_generated_at=ai_generated_at,
        )
    except LLMUnavailable as exc:
        logger.warning("Local AI unavailable, using fallback briefing: %s", exc)
        return BriefingResult(
            markdown=fallback_briefing(context),
            mode="basic",
            generated_at=generated_at,
            notice="Local AI unavailable - using basic briefing.",
            last_ai_markdown=last_ai_markdown or None,
            last_ai_generated_at=last_ai_generated_at or None,
        )
