from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import SERVICE_STATUSES, ServiceCard
from app.schemas import ServiceCreate, ServiceUpdate, model_data
from app.services.healthchecks import update_service_health

router = APIRouter(prefix="/api/services", tags=["services"])


def _get_service(session: Session, service_id: int) -> ServiceCard:
    service = session.get(ServiceCard, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.get("")
def list_services(session: Session = Depends(get_session)) -> list[ServiceCard]:
    return session.exec(select(ServiceCard).order_by(ServiceCard.sort_order, ServiceCard.name)).all()


@router.post("")
def create_service(payload: ServiceCreate, session: Session = Depends(get_session)) -> ServiceCard:
    data = model_data(payload)
    data["name"] = data["name"].strip()
    if not data["name"]:
        raise HTTPException(status_code=422, detail="Service name is required")
    service = ServiceCard(**data)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@router.patch("/{service_id}")
def update_service(service_id: int, payload: ServiceUpdate, session: Session = Depends(get_session)) -> ServiceCard:
    service = _get_service(session, service_id)
    data = model_data(payload, exclude_unset=True)
    if "name" in data:
        data["name"] = data["name"].strip()
        if not data["name"]:
            raise HTTPException(status_code=422, detail="Service name is required")
    for key, value in data.items():
        setattr(service, key, value)
    if service.last_status not in SERVICE_STATUSES:
        service.last_status = "unknown"
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@router.delete("/{service_id}")
def delete_service(service_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    service = _get_service(session, service_id)
    session.delete(service)
    session.commit()
    return {"ok": True}


@router.post("/check")
async def check_services(session: Session = Depends(get_session)) -> list[ServiceCard]:
    services = session.exec(select(ServiceCard).order_by(ServiceCard.sort_order, ServiceCard.name)).all()
    checked: list[ServiceCard] = []
    for service in services:
        checked.append(await update_service_health(session, service))
    return checked

