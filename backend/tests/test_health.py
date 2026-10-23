from collections.abc import Generator
from typing import Any

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


def test_health_endpoint_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_reports_database(client: TestClient) -> None:
    response = client.get("/health")
    assert response.json() == {"status": "ok", "database": "ok"}


class _BrokenSession:
    def execute(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("database is unreachable")


def test_health_endpoint_reports_degraded() -> None:
    def override_get_db() -> Generator[Any, None, None]:
        yield _BrokenSession()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            response = test_client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "unreachable"}
