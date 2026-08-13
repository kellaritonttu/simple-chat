async def test_create_user(client, mock_firebase):
    response = await client.post(
        "/users/",
        json={"id": "test-uid-123", "display_name": "John"},
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 201