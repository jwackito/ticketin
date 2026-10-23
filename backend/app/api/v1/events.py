import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.event import EventPage, EventRead
from app.services import events as events_service

router = APIRouter(prefix="/events", tags=["events"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=EventPage)
def list_events(
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> EventPage:
    items, total = events_service.list_published(db, limit, offset)
    return EventPage(
        items=[EventRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: uuid.UUID, db: DbSession) -> EventRead:
    event = events_service.get_published(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventRead.model_validate(event)
