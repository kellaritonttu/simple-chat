AUTH_HEADER = {"Authorization": "Bearer fake-token"}

from repository.message import get_message_by_id

# ── GET /messages ─────────────────────────────────────────────────────────────

async def test_list_messages_empty(client, mock_firebase):
    response = await client.get("/messages/", headers=AUTH_HEADER)
    assert response.status_code == 200
    assert response.json() == []


async def test_list_messages(client, mock_firebase, saved_message):
    response = await client.get("/messages/", headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Hello world"


# ── GET /messages/{id} ────────────────────────────────────────────────────────

async def test_get_message(client, mock_firebase, saved_message):
    response = await client.get(f"/messages/{saved_message.id}", headers=AUTH_HEADER)
    assert response.status_code == 200
    assert response.json()["text"] == "Hello world"


async def test_get_message_not_found(client, mock_firebase):
    response = await client.get("/messages/999", headers=AUTH_HEADER)
    assert response.status_code == 404


# ── POST /messages ────────────────────────────────────────────────────────────

async def test_create_message(client, mock_firebase, saved_user, db_session):
    response = await client.post(
        "/messages/",
        json={"text": "Test message"},
        headers=AUTH_HEADER
    )
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Test message"
    assert body["user_id"] == "test-uid-123"

    saved = await get_message_by_id(db_session, body["id"])
    assert saved is not None


async def test_create_message_unauthorized(client):
    response = await client.post(
        "/messages/",
        json={"text": "Test message"},
    )
    assert response.status_code == 422  # missing Authorization header


# ── PATCH /messages/{id} ──────────────────────────────────────────────────────

async def test_update_message(client, mock_firebase, saved_message, db_session):
    response = await client.patch(
        f"/messages/{saved_message.id}",
        params={"text": "Updated"},
        headers=AUTH_HEADER
    )
    assert response.status_code == 200
    assert response.json()["text"] == "Updated"


async def test_update_message_forbidden(client, mock_firebase_other, saved_message):
    response = await client.patch(
        f"/messages/{saved_message.id}",
        params={"text": "Updated"},
        headers=AUTH_HEADER
    )
    assert response.status_code == 403


async def test_update_message_not_found(client, mock_firebase):
    response = await client.patch("/messages/999", params={"text": "x"}, headers=AUTH_HEADER)
    assert response.status_code == 404


# ── DELETE /messages/{id} ─────────────────────────────────────────────────────

async def test_delete_message(client, mock_firebase, saved_message, db_session):
    response = await client.delete(f"/messages/{saved_message.id}", headers=AUTH_HEADER)
    assert response.status_code == 204

    saved = await get_message_by_id(db_session, saved_message.id)
    assert saved is None


async def test_delete_message_forbidden(client, mock_firebase_other, saved_message):
    response = await client.delete(
        f"/messages/{saved_message.id}",
        headers=AUTH_HEADER
    )
    assert response.status_code == 403


async def test_delete_message_not_found(client, mock_firebase):
    response = await client.delete("/messages/999", headers=AUTH_HEADER)
    assert response.status_code == 404