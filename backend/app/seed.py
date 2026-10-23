"""Insert demo events for local development.

Idempotent: rows use fixed UUIDs and are written with ``session.merge``, so
re-running updates them instead of duplicating. Never runs at application
startup and is not used by tests.
"""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.event import Event

_DEMO_ROWS: list[tuple[str, str, timedelta]] = [
    ("Spring Hackathon", "published", timedelta(days=7)),
    ("Intro to FastAPI", "published", timedelta(days=14)),
    ("Summer Meetup", "draft", timedelta(days=21)),
    ("Last Year's Conference", "published", timedelta(days=-7)),
]


def _event_id(index: int) -> uuid.UUID:
    return uuid.UUID(f"00000000-0000-0000-0000-0000000000{index:02d}")


def seed(session: Session) -> int:
    now = datetime.now(UTC)
    for index, (title, status, offset) in enumerate(_DEMO_ROWS, start=1):
        session.merge(
            Event(
                id=_event_id(index),
                title=title,
                description=f"{title} demo event",
                venue="Main Hall",
                starts_at=now + offset,
                capacity=100,
                status=status,
            )
        )
    session.commit()
    return len(_DEMO_ROWS)


def main() -> None:
    with SessionLocal() as session:
        count = seed(session)
    print(f"Seeded {count} demo events.")


if __name__ == "__main__":
    main()
