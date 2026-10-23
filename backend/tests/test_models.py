import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.event import Event


def _event(**overrides: Any) -> Event:
    data: dict[str, Any] = {
        "id": uuid.uuid4(),
        "title": "Test Event",
        "venue": "Main Hall",
        "starts_at": datetime.now(UTC) + timedelta(days=1),
        "capacity": 10,
        "status": "published",
    }
    data.update(overrides)
    return Event(**data)


def test_capacity_must_be_positive(db_session: Session) -> None:
    db_session.add(_event(capacity=0))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_status_must_be_known(db_session: Session) -> None:
    db_session.add(_event(status="bogus"))
    with pytest.raises(IntegrityError):
        db_session.flush()
