import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models.event import Event


def make_event(**overrides: Any) -> Event:
    now = datetime.now(UTC)
    data: dict[str, Any] = {
        "id": uuid.uuid4(),
        "title": "Test Event",
        "description": "A test event",
        "venue": "Main Hall",
        "starts_at": now + timedelta(days=1),
        "capacity": 10,
        "status": "published",
    }
    data.update(overrides)
    return Event(**data)


def add_event(db: Session, **overrides: Any) -> Event:
    event = make_event(**overrides)
    db.add(event)
    db.flush()
    return event
