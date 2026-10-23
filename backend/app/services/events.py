import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.event import Event

PUBLISHED = "published"


def _now() -> datetime:
    return datetime.now(UTC)


def list_published(db: Session, limit: int, offset: int) -> tuple[list[Event], int]:
    """Return a page of published upcoming events and the total matching count."""
    base = select(Event).where(Event.status == PUBLISHED, Event.starts_at >= _now())
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    items = list(
        db.scalars(
            base.order_by(Event.starts_at.asc(), Event.id.asc()).limit(limit).offset(offset)
        )
    )
    return items, total


def get_published(db: Session, event_id: uuid.UUID) -> Event | None:
    """Return a published event by id regardless of start time, else ``None``."""
    return db.scalar(select(Event).where(Event.id == event_id, Event.status == PUBLISHED))
