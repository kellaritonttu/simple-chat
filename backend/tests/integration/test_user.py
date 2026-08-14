import pytest
from repository.user import get_user_by_id

# ── POST /users/ ─────────────────────────────────────────────────────────────

async def test_create_user(client, mock_firebase):
    """Test creating a new user with google_display_name and app_display_name."""
    response = await client.post(
        "/users/",
        json={
            "id": "test-uid-123",
            "google_display_name": "John Doe",
            "app_display_name": "John Doe"
        },
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "test-uid-123"
    assert data["google_display_name"] == "John Doe"
    assert data["app_display_name"] == "John Doe"

async def test_create_user_unauthorized(client):
    """Test creating a user without authentication fails."""
    response = await client.post(
        "/users/",
        json={
            "id": "test-uid-123",
            "google_display_name": "John Doe",
            "app_display_name": "John Doe"
        }
    )
    assert response.status_code == 403

# ── GET /users/me ────────────────────────────────────────────────────────────

async def test_get_current_user(client, mock_firebase, saved_user):
    """Test fetching the current user's data."""
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == saved_user.id
    assert data["google_display_name"] == saved_user.google_display_name
    assert data["app_display_name"] == saved_user.app_display_name

async def test_get_current_user_unauthorized(client):
    """Test fetching current user without authentication fails."""
    response = await client.get("/users/me")
    assert response.status_code == 403

# ── PATCH /users/me ───────────────────────────────────────────────────────────

async def test_update_user_display_name(client, mock_firebase, saved_user, db_session):
    """Test updating the user's app_display_name."""
    new_name = "New Display Name"
    response = await client.patch(
        "/users/me",
        json={"app_display_name": new_name},
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["app_display_name"] == new_name

    # Verify the update in the database
    updated_user = await get_user_by_id(db_session, saved_user.id)
    assert updated_user is not None
    assert updated_user.app_display_name == new_name

async def test_update_user_unauthorized(client):
    """Test updating user without authentication fails."""
    response = await client.patch(
        "/users/me",
        json={"app_display_name": "New Display Name"}
    )
    assert response.status_code == 403

# ── DELETE /users/me ─────────────────────────────────────────────────────────

async def test_delete_user(client, mock_firebase, saved_user, db_session):
    """Test deleting the current user."""
    response = await client.delete(
        "/users/me",
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 204

    # Verify the user is deleted
    deleted_user = await get_user_by_id(db_session, saved_user.id)
    assert deleted_user is None

async def test_delete_user_unauthorized(client):
    """Test deleting user without authentication fails."""
    response = await client.delete("/users/me")
    assert response.status_code == 403