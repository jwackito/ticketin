from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.seed import seed


def _count(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(Event)) or 0


def test_seed_is_idempotent(db_session: Session) -> None:
    seed(db_session)
    first = _count(db_session)

    seed(db_session)
    second = _count(db_session)

    assert first == 4
    assert second == 4
