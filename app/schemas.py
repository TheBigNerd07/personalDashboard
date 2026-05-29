from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel


class TaskCreate(SQLModel):
    title: str
    description: str = ""
    category: str = "unknown"
    priority: str = "normal"
    status: str = "inbox"
    due_date: Optional[date] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None


class ProjectCreate(SQLModel):
    name: str
    description: str = ""
    category: str = "Personal"
    status: str = "active"
    next_action: str = ""
    link: Optional[str] = None


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    next_action: Optional[str] = None
    link: Optional[str] = None


class NoteCreate(SQLModel):
    title: str
    body: str = ""
    tags: str = ""


class NoteUpdate(SQLModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[str] = None


class ServiceCreate(SQLModel):
    name: str
    url: str = ""
    description: str = ""
    category: str = "homelab"
    healthcheck_url: Optional[str] = None
    sort_order: int = 100


class ServiceUpdate(SQLModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    healthcheck_url: Optional[str] = None
    sort_order: Optional[int] = None


def model_data(model: SQLModel, *, exclude_unset: bool = False) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_unset=exclude_unset)
    return model.dict(exclude_unset=exclude_unset)

