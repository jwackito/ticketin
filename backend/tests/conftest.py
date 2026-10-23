import os
from collections.abc import Generator
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session

from alembic import command

DEFAULT_TEST_URL = "postgresql://ticketin:ticketin@localhost:5432/ticketin_test"
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_URL)

# Point the application at the test database before any app module is imported.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402

BACKEND_DIR = Path(__file__).resolve().parents[1]


def _ensure_database(url: str) -> None:
    parsed = make_url(url)
    if parsed.database is None:
        raise RuntimeError("TEST_DATABASE_URL must include a database name")
    maintenance = parsed.set(database="postgres")
    engine = create_engine(maintenance, isolation_level="AUTOCOMMIT")
    with engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": parsed.database},
        ).scalar()
        if not exists:
            connection.execute(text(f'CREATE DATABASE "{parsed.database}"'))
    engine.dispose()


def _run_migrations(url: str) -> None:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    _ensure_database(TEST_DATABASE_URL)
    _run_migrations(TEST_DATABASE_URL)
    test_engine = create_engine(TEST_DATABASE_URL)
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
