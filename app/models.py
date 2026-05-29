from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.utcnow()


TASK_CATEGORIES = {
    "school",
    "stride_shots",
    "homelab",
    "personal",
    "business",
    "idea",
    "wishlist",
    "music",
    "photography",
    "unknown",
}
TASK_PRIORITIES = {"low", "normal", "high", "urgent"}
TASK_STATUSES = {"inbox", "active", "completed", "archived"}
PROJECT_STATUSES = {"active", "paused", "completed", "archived"}
SERVICE_STATUSES = {"unknown", "up", "down"}


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1)
    description: str = ""
    category: str = Field(default="unknown", index=True)
    priority: str = Field(default="normal", index=True)
    status: str = Field(default="inbox", index=True)
    due_date: Optional[date] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    completed_at: Optional[datetime] = None


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1)
    description: str = ""
    category: str = Field(default="Personal", index=True)
    status: str = Field(default="active", index=True)
    next_action: str = ""
    link: Optional[str] = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1)
    body: str = ""
    tags: str = ""
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ServiceCard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1)
    url: str = ""
    description: str = ""
    category: str = Field(default="homelab", index=True)
    healthcheck_url: Optional[str] = None
    last_status: str = Field(default="unknown", index=True)
    last_checked_at: Optional[datetime] = None
    sort_order: int = Field(default=100, index=True)


class Setting(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str = ""
    updated_at: datetime = Field(default_factory=utcnow)

