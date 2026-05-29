from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Note, utcnow
from app.schemas import NoteCreate, NoteUpdate, model_data

router = APIRouter(prefix="/api/notes", tags=["notes"])


def _get_note(session: Session, note_id: int) -> Note:
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("")
def list_notes(session: Session = Depends(get_session)) -> list[Note]:
    return session.exec(select(Note).order_by(Note.updated_at.desc())).all()


@router.post("")
def create_note(payload: NoteCreate, session: Session = Depends(get_session)) -> Note:
    data = model_data(payload)
    data["title"] = data["title"].strip()
    if not data["title"]:
        raise HTTPException(status_code=422, detail="Note title is required")
    note = Note(**data)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.patch("/{note_id}")
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)) -> Note:
    note = _get_note(session, note_id)
    data = model_data(payload, exclude_unset=True)
    if "title" in data:
        data["title"] = data["title"].strip()
        if not data["title"]:
            raise HTTPException(status_code=422, detail="Note title is required")
    for key, value in data.items():
        setattr(note, key, value)
    note.updated_at = utcnow()
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    note = _get_note(session, note_id)
    session.delete(note)
    session.commit()
    return {"ok": True}

