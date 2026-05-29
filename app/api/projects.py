from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import PROJECT_STATUSES, Project, utcnow
from app.schemas import ProjectCreate, ProjectUpdate, model_data

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _get_project(session: Session, project_id: int) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("")
def list_projects(session: Session = Depends(get_session)) -> list[Project]:
    return session.exec(select(Project).order_by(Project.status, Project.category, Project.name)).all()


@router.post("")
def create_project(payload: ProjectCreate, session: Session = Depends(get_session)) -> Project:
    data = model_data(payload)
    data["name"] = data["name"].strip()
    if not data["name"]:
        raise HTTPException(status_code=422, detail="Project name is required")
    if data["status"] not in PROJECT_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid project status")
    project = Project(**data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.patch("/{project_id}")
def update_project(project_id: int, payload: ProjectUpdate, session: Session = Depends(get_session)) -> Project:
    project = _get_project(session, project_id)
    data = model_data(payload, exclude_unset=True)
    if "name" in data:
        data["name"] = data["name"].strip()
        if not data["name"]:
            raise HTTPException(status_code=422, detail="Project name is required")
    if "status" in data and data["status"] not in PROJECT_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid project status")
    for key, value in data.items():
        setattr(project, key, value)
    project.updated_at = utcnow()
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    project = _get_project(session, project_id)
    session.delete(project)
    session.commit()
    return {"ok": True}

