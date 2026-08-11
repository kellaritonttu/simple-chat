import pytest
from httpx import AsyncClient
from repository.message import get_all_messages, get_message_by_id


# ── GET /messages ─────────────────────────────────────────────────────────────

async def test_list_messages_empty(client: AsyncClient):
    response = await client.get("/messages/")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_messages(client: AsyncClient, saved_message):
    response = await client.get("/messages/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Hello world"


# ── GET /messages/{id} ────────────────────────────────────────────────────────

async def test_get_message(client: AsyncClient, saved_message):
    response = await client.get(f"/messages/{saved_message.id}")
    assert response.status_code == 200
    assert response.json()["text"] == "Hello world"


async def test_get_message_not_found(client: AsyncClient):
    response = await client.get("/messages/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


# ── POST /messages ────────────────────────────────────────────────────────────

async def test_create_message(client: AsyncClient, db_session):
    response = await client.post("/messages/", json={"text": "Test message"})
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Test message"
    assert body["id"] is not None
    assert body["created_at"] is not None

    saved = await get_message_by_id(db_session, body["id"])
    assert saved is not None
    assert saved.text == "Test message"


# ── PATCH /messages/{id} ──────────────────────────────────────────────────────

async def test_update_message(client: AsyncClient, saved_message, db_session):
    response = await client.patch(
        f"/messages/{saved_message.id}",
        params={"update": "Updated text"}
    )
    assert response.status_code == 200
    assert response.json()["text"] == "Updated text"

    saved = await get_message_by_id(db_session, saved_message.id)
    assert saved.text == "Updated text"


async def test_update_message_not_found(client: AsyncClient):
    response = await client.patch("/messages/999", params={"update": "x"})
    assert response.status_code == 404


# ── DELETE /messages/{id} ─────────────────────────────────────────────────────

async def test_delete_message(client: AsyncClient, saved_message, db_session):
    response = await client.delete(f"/messages/{saved_message.id}")
    assert response.status_code == 204

    saved = await get_message_by_id(db_session, saved_message.id)
    assert saved is None


async def test_delete_message_not_found(client: AsyncClient):
    response = await client.delete("/messages/999")
    assert response.status_code == 404