import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.factories import add_event

BASE = "/api/v1/events"


def test_list_default_page(client: TestClient, db_session: Session) -> None:
    for index in range(3):
        add_event(db_session, title=f"Event {index}")

    response = client.get(BASE)

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 3
    assert body["total"] == 3
    assert body["limit"] == 20
    assert body["offset"] == 0


def test_list_explicit_page(client: TestClient, db_session: Session) -> None:
    for index in range(3):
        add_event(db_session, title=f"Event {index}")

    response = client.get(BASE, params={"limit": 1, "offset": 1})

    body = response.json()
    assert len(body["items"]) == 1
    assert body["total"] == 3
    assert body["limit"] == 1
    assert body["offset"] == 1


def test_list_offset_past_end(client: TestClient, db_session: Session) -> None:
    add_event(db_session)

    body = client.get(BASE, params={"offset": 99}).json()

    assert body["items"] == []
    assert body["total"] == 1


def test_list_empty_catalog(client: TestClient) -> None:
    body = client.get(BASE).json()

    assert body["items"] == []
    assert body["total"] == 0


def test_list_excludes_drafts_and_past(client: TestClient, db_session: Session) -> None:
    add_event(db_session, title="Visible")
    add_event(db_session, title="Draft", status="draft")
    add_event(
        db_session,
        title="Past",
        starts_at=datetime.now(UTC) - timedelta(days=1),
    )

    body = client.get(BASE).json()

    assert body["total"] == 1
    assert [item["title"] for item in body["items"]] == ["Visible"]


def test_list_orders_by_start_time(client: TestClient, db_session: Session) -> None:
    now = datetime.now(UTC)
    add_event(db_session, title="Later", starts_at=now + timedelta(days=5))
    add_event(db_session, title="Sooner", starts_at=now + timedelta(days=1))

    body = client.get(BASE).json()

    assert [item["title"] for item in body["items"]] == ["Sooner", "Later"]


def test_list_rejects_invalid_limit(client: TestClient) -> None:
    assert client.get(BASE, params={"limit": 0}).status_code == 422
    assert client.get(BASE, params={"limit": 101}).status_code == 422


def test_list_rejects_negative_offset(client: TestClient) -> None:
    assert client.get(BASE, params={"offset": -1}).status_code == 422


def test_detail_returns_published_event(client: TestClient, db_session: Session) -> None:
    event = add_event(db_session, title="Detail")

    response = client.get(f"{BASE}/{event.id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Detail"


def test_detail_returns_past_published_event(
    client: TestClient, db_session: Session
) -> None:
    event = add_event(
        db_session,
        title="Past Published",
        starts_at=datetime.now(UTC) - timedelta(days=1),
    )

    response = client.get(f"{BASE}/{event.id}")

    assert response.status_code == 200


def test_detail_draft_is_not_found(client: TestClient, db_session: Session) -> None:
    event = add_event(db_session, status="draft")

    response = client.get(f"{BASE}/{event.id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_detail_unknown_is_not_found(client: TestClient) -> None:
    response = client.get(f"{BASE}/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_detail_malformed_id_is_rejected(client: TestClient) -> None:
    assert client.get(f"{BASE}/not-a-uuid").status_code == 422
