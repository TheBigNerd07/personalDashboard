from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional

from app.database import get_session
from app.models import TASK_CATEGORIES, TASK_PRIORITIES, TASK_STATUSES, Task, utcnow
from app.schemas import TaskCreate, TaskUpdate, model_data

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _validate_task_values(task_data: dict) -> None:
    if "category" in task_data and task_data["category"] not in TASK_CATEGORIES:
        raise HTTPException(status_code=422, detail="Invalid task category")
    if "priority" in task_data and task_data["priority"] not in TASK_PRIORITIES:
        raise HTTPException(status_code=422, detail="Invalid task priority")
    if "status" in task_data and task_data["status"] not in TASK_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid task status")


def _get_task(session: Session, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("")
def list_tasks(
    status: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
) -> list[Task]:
    statement = select(Task)
    if status:
        statement = statement.where(Task.status == status)
    if category:
        statement = statement.where(Task.category == category)
    return session.exec(statement.order_by(Task.status, Task.due_date, Task.created_at)).all()


@router.post("")
def create_task(payload: TaskCreate, session: Session = Depends(get_session)) -> Task:
    data = model_data(payload)
    data["title"] = data["title"].strip()
    if not data["title"]:
        raise HTTPException(status_code=422, detail="Task title is required")
    _validate_task_values(data)
    task = Task(**data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{task_id}")
def read_task(task_id: int, session: Session = Depends(get_session)) -> Task:
    return _get_task(session, task_id)


@router.patch("/{task_id}")
def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)) -> Task:
    task = _get_task(session, task_id)
    data = model_data(payload, exclude_unset=True)
    if "title" in data:
        data["title"] = data["title"].strip()
        if not data["title"]:
            raise HTTPException(status_code=422, detail="Task title is required")
    _validate_task_values(data)
    for key, value in data.items():
        setattr(task, key, value)
    if task.status == "completed" and task.completed_at is None:
        task.completed_at = utcnow()
    if task.status != "completed":
        task.completed_at = None
    task.updated_at = utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    task = _get_task(session, task_id)
    session.delete(task)
    session.commit()
    return {"ok": True}


@router.post("/{task_id}/complete")
def complete_task(task_id: int, session: Session = Depends(get_session)) -> Task:
    task = _get_task(session, task_id)
    task.status = "completed"
    task.completed_at = utcnow()
    task.updated_at = utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
