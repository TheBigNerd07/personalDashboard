from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from markupsafe import Markup, escape
from sqlmodel import Session, select

from app.auth import verify_password
from app.config import get_settings
from app.database import get_session, get_setting, set_setting
from app.models import (
    PROJECT_STATUSES,
    TASK_CATEGORIES,
    TASK_PRIORITIES,
    TASK_STATUSES,
    Note,
    Project,
    ServiceCard,
    Task,
    utcnow,
)
from app.services.briefing import create_daily_briefing
from app.services.healthchecks import update_service_health
from app.services.weather import fetch_weather

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _markdown_to_html(value: Optional[str]) -> Markup:
    if not value:
        return Markup("")
    html: list[str] = []
    in_list = False
    for raw_line in value.splitlines():
        line = raw_line.strip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            continue
        if line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{escape(line[3:])}</h3>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[2:])}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{escape(line)}</p>")
    if in_list:
        html.append("</ul>")
    return Markup("\n".join(html))


templates.env.filters["briefing_markdown"] = _markdown_to_html


def _redirect(anchor: str = "") -> RedirectResponse:
    suffix = f"#{anchor}" if anchor else ""
    return RedirectResponse(url=f"/{suffix}", status_code=303)


def _optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _date_or_none(value: Optional[str]):
    value = _optional(value)
    if not value:
        return None
    return date.fromisoformat(value)


def _int_or_default(value: Optional[str], default: int) -> int:
    try:
        return int(value or default)
    except ValueError:
        return default


def _task_focus_key(task: Task):
    priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    return (priority_order.get(task.priority, 4), task.due_date or date.max, task.created_at)


def _project_sort_key(project: Project):
    status_order = {"active": 0, "paused": 1, "completed": 2, "archived": 3}
    return (status_order.get(project.status, 4), project.category, project.name)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/login")
def login_form(request: Request):
    settings = get_settings()
    if not settings.auth_enabled:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "app_name": settings.app_name, "error": None})


@router.post("/login")
async def login(request: Request):
    settings = get_settings()
    form = await request.form()
    if verify_password(str(form.get("password", "")), settings.app_password):
        request.session["authenticated"] = True
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "app_name": settings.app_name, "error": "Incorrect password."},
        status_code=401,
    )


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@router.get("/")
async def index(
    request: Request,
    status: Optional[str] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session),
):
    settings = get_settings()
    try:
        now = datetime.now(ZoneInfo(settings.weather_timezone))
    except Exception:
        now = datetime.now()

    task_statement = select(Task)
    if status:
        task_statement = task_statement.where(Task.status == status)
    else:
        task_statement = task_statement.where(Task.status != "archived")
    if category:
        task_statement = task_statement.where(Task.category == category)

    tasks = session.exec(task_statement.order_by(Task.status, Task.due_date, Task.created_at)).all()
    active_tasks = session.exec(select(Task).where(Task.status.in_(["inbox", "active"]))).all()
    top_tasks = sorted(active_tasks, key=_task_focus_key)[:3]
    today = date.today()
    upcoming_deadlines = sorted(
        [
            task
            for task in active_tasks
            if task.due_date is not None and today <= task.due_date <= today + timedelta(days=14)
        ],
        key=_task_focus_key,
    )
    projects = session.exec(select(Project).where(Project.status != "archived").order_by(Project.status, Project.category, Project.name)).all()
    notes = session.exec(select(Note).order_by(Note.updated_at.desc())).all()
    services = session.exec(select(ServiceCard).order_by(ServiceCard.sort_order, ServiceCard.name)).all()
    weather = await fetch_weather(settings)
    briefing = await create_daily_briefing(session, weather=weather, use_ai=False)

    service_summary = {
        "up": len([service for service in services if service.last_status == "up"]),
        "down": len([service for service in services if service.last_status == "down"]),
        "unknown": len([service for service in services if service.last_status == "unknown"]),
        "total": len(services),
    }
    active_projects = sorted([project for project in projects if project.status == "active"], key=_project_sort_key)
    paused_projects = sorted([project for project in projects if project.status == "paused"], key=_project_sort_key)
    school_deadlines = sorted(
        [
            task
            for task in active_tasks
            if task.category == "school" and task.due_date is not None and task.due_date <= today + timedelta(days=30)
        ],
        key=_task_focus_key,
    )
    stride_projects = [project for project in active_projects if project.category.lower() == "stride shots"]
    homelab_projects = [project for project in active_projects if project.category.lower() == "homelab"]
    school_projects = [project for project in active_projects if project.category.lower() == "school"]
    stride_items = sorted([task for task in active_tasks if task.category == "stride_shots"], key=_task_focus_key)[:4]
    homelab_items = sorted([task for task in active_tasks if task.category == "homelab"], key=_task_focus_key)[:4]
    attention_items = [task for task in top_tasks if task.priority in {"urgent", "high"}]
    down_services = [service for service in services if service.last_status == "down"]
    quick_services = services[:8]
    recent_notes = notes[:4]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "auth_enabled": settings.auth_enabled,
            "now": now,
            "today_focus": get_setting(session, "todays_focus", ""),
            "top_tasks": top_tasks,
            "upcoming_deadlines": upcoming_deadlines,
            "tasks": tasks,
            "projects": projects,
            "notes": notes,
            "services": services,
            "weather": weather,
            "briefing": briefing,
            "latest_ai_notice": get_setting(session, "latest_ai_notice", ""),
            "llm_enabled": settings.llm_enabled,
            "task_categories": sorted(TASK_CATEGORIES),
            "task_priorities": ["urgent", "high", "normal", "low"],
            "task_statuses": ["inbox", "active", "completed", "archived"],
            "project_statuses": ["active", "paused", "completed", "archived"],
            "selected_status": status or "",
            "selected_category": category or "",
            "active_projects": active_projects,
            "paused_projects": paused_projects,
            "school_deadlines": school_deadlines,
            "stride_items": stride_items,
            "homelab_items": homelab_items,
            "stride_projects": stride_projects,
            "homelab_projects": homelab_projects,
            "school_projects": school_projects,
            "attention_items": attention_items,
            "down_services": down_services,
            "quick_services": quick_services,
            "recent_notes": recent_notes,
            "service_summary": service_summary,
        },
    )


@router.post("/focus")
async def update_focus(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    set_setting(session, "todays_focus", str(form.get("todays_focus", "")).strip())
    return _redirect("focus")


@router.post("/tasks")
async def create_task(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    task = Task(
        title=str(form.get("title", "")).strip(),
        description=str(form.get("description", "")).strip(),
        category=str(form.get("category", "unknown")),
        priority=str(form.get("priority", "normal")),
        status=str(form.get("status", "inbox")),
        due_date=_date_or_none(str(form.get("due_date", ""))),
    )
    if task.title:
        session.add(task)
        session.commit()
    return _redirect("tasks")


@router.post("/tasks/{task_id}/update")
async def update_task(task_id: int, request: Request, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        return _redirect("tasks")
    form = await request.form()
    task.title = str(form.get("title", task.title)).strip() or task.title
    task.description = str(form.get("description", "")).strip()
    task.category = str(form.get("category", task.category))
    task.priority = str(form.get("priority", task.priority))
    task.status = str(form.get("status", task.status))
    task.due_date = _date_or_none(str(form.get("due_date", "")))
    task.completed_at = utcnow() if task.status == "completed" and task.completed_at is None else task.completed_at
    if task.status != "completed":
        task.completed_at = None
    task.updated_at = utcnow()
    session.add(task)
    session.commit()
    return _redirect("tasks")


@router.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is not None:
        task.status = "completed"
        task.completed_at = utcnow()
        task.updated_at = utcnow()
        session.add(task)
        session.commit()
    return _redirect("tasks")


@router.post("/tasks/{task_id}/delete")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is not None:
        session.delete(task)
        session.commit()
    return _redirect("tasks")


@router.post("/projects")
async def create_project(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    project = Project(
        name=str(form.get("name", "")).strip(),
        description=str(form.get("description", "")).strip(),
        category=str(form.get("category", "Personal")).strip() or "Personal",
        status=str(form.get("status", "active")),
        next_action=str(form.get("next_action", "")).strip(),
        link=_optional(str(form.get("link", ""))),
    )
    if project.name:
        session.add(project)
        session.commit()
    return _redirect("projects")


@router.post("/projects/{project_id}/update")
async def update_project(project_id: int, request: Request, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is None:
        return _redirect("projects")
    form = await request.form()
    project.name = str(form.get("name", project.name)).strip() or project.name
    project.description = str(form.get("description", "")).strip()
    project.category = str(form.get("category", project.category)).strip() or project.category
    project.status = str(form.get("status", project.status))
    project.next_action = str(form.get("next_action", "")).strip()
    project.link = _optional(str(form.get("link", "")))
    project.updated_at = utcnow()
    session.add(project)
    session.commit()
    return _redirect("projects")


@router.post("/projects/{project_id}/delete")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is not None:
        session.delete(project)
        session.commit()
    return _redirect("projects")


@router.post("/notes")
async def create_note(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    note = Note(
        title=str(form.get("title", "")).strip(),
        body=str(form.get("body", "")).strip(),
        tags=str(form.get("tags", "")).strip(),
    )
    if note.title:
        session.add(note)
        session.commit()
    return _redirect("notes")


@router.post("/notes/{note_id}/update")
async def update_note(note_id: int, request: Request, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        return _redirect("notes")
    form = await request.form()
    note.title = str(form.get("title", note.title)).strip() or note.title
    note.body = str(form.get("body", "")).strip()
    note.tags = str(form.get("tags", "")).strip()
    note.updated_at = utcnow()
    session.add(note)
    session.commit()
    return _redirect("notes")


@router.post("/notes/{note_id}/delete")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is not None:
        session.delete(note)
        session.commit()
    return _redirect("notes")


@router.post("/services")
async def create_service(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    service = ServiceCard(
        name=str(form.get("name", "")).strip(),
        url=str(form.get("url", "")).strip(),
        description=str(form.get("description", "")).strip(),
        category=str(form.get("category", "homelab")).strip() or "homelab",
        healthcheck_url=_optional(str(form.get("healthcheck_url", ""))),
        sort_order=_int_or_default(str(form.get("sort_order", "")), 100),
    )
    if service.name:
        session.add(service)
        session.commit()
    return _redirect("services")


@router.post("/services/{service_id}/update")
async def update_service(service_id: int, request: Request, session: Session = Depends(get_session)):
    service = session.get(ServiceCard, service_id)
    if service is None:
        return _redirect("services")
    form = await request.form()
    service.name = str(form.get("name", service.name)).strip() or service.name
    service.url = str(form.get("url", "")).strip()
    service.description = str(form.get("description", "")).strip()
    service.category = str(form.get("category", service.category)).strip() or service.category
    service.healthcheck_url = _optional(str(form.get("healthcheck_url", "")))
    service.sort_order = _int_or_default(str(form.get("sort_order", "")), service.sort_order)
    session.add(service)
    session.commit()
    return _redirect("services")


@router.post("/services/{service_id}/delete")
def delete_service(service_id: int, session: Session = Depends(get_session)):
    service = session.get(ServiceCard, service_id)
    if service is not None:
        session.delete(service)
        session.commit()
    return _redirect("services")


@router.post("/services/check")
async def check_service_cards(session: Session = Depends(get_session)):
    services = session.exec(select(ServiceCard).order_by(ServiceCard.sort_order, ServiceCard.name)).all()
    for service in services:
        await update_service_health(session, service)
    return _redirect("services")
