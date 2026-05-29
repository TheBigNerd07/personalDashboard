from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session, set_setting
from app.models import Setting

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def list_settings(session: Session = Depends(get_session)) -> dict[str, str]:
    settings = session.exec(select(Setting).order_by(Setting.key)).all()
    return {setting.key: setting.value for setting in settings}


@router.patch("")
def update_settings(payload: dict[str, str], session: Session = Depends(get_session)) -> dict[str, str]:
    for key, value in payload.items():
        set_setting(session, key, "" if value is None else str(value))
    settings = session.exec(select(Setting).order_by(Setting.key)).all()
    return {setting.key: setting.value for setting in settings}

