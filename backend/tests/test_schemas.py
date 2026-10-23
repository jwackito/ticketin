import uuid
from datetime import UTC, datetime, timedelta

from app.models.event import Event
from app.schemas.event import EventPage, EventRead


def _event() -> Event:
    now = datetime.now(UTC)
    return Event(
        id=uuid.uuid4(),
        title="Serializable Event",
        description=None,
        venue="Main Hall",
        starts_at=now + timedelta(days=1),
        capacity=5,
        status="published",
        created_at=now,
        updated_at=now,
    )


def test_event_read_serializes_orm_object() -> None:
    read = EventRead.model_validate(_event())
    assert read.title == "Serializable Event"
    assert read.description is None
    assert read.capacity == 5


def test_event_page_envelope() -> None:
    page = EventPage(items=[], total=0, limit=20, offset=0)
    dumped = page.model_dump()
    assert dumped["items"] == []
    assert dumped["total"] == 0
    assert dumped["limit"] == 20
    assert dumped["offset"] == 0
