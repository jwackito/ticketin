from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.services import events as events_service
from tests.factories import add_event


def test_list_excludes_drafts_and_past(db_session: Session) -> None:
    visible = add_event(db_session, title="Visible")
    add_event(db_session, title="Draft", status="draft")
    add_event(
        db_session,
        title="Past",
        starts_at=datetime.now(UTC) - timedelta(days=1),
    )

    items, total = events_service.list_published(db_session, limit=20, offset=0)

    assert total == 1
    assert [event.id for event in items] == [visible.id]


def test_list_orders_by_starts_at_then_id(db_session: Session) -> None:
    now = datetime.now(UTC)
    second = add_event(db_session, title="Second", starts_at=now + timedelta(days=5))
    first = add_event(db_session, title="First", starts_at=now + timedelta(days=1))

    items, _ = events_service.list_published(db_session, limit=20, offset=0)

    assert [event.id for event in items] == [first.id, second.id]


def test_get_published_is_time_independent(db_session: Session) -> None:
    past = add_event(
        db_session,
        title="Past",
        starts_at=datetime.now(UTC) - timedelta(days=1),
    )
    draft = add_event(db_session, title="Draft", status="draft")

    assert events_service.get_published(db_session, past.id) is not None
    assert events_service.get_published(db_session, draft.id) is None
