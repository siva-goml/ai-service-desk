import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_delete_ticket(client):
    create_payload = {
        "title": "Ticket to delete",
        "description": "This ticket will be deleted",
    }

    create_response = await client.post(
        "/tickets/",
        json=create_payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Ticket deleted successfully"


@pytest.mark.asyncio
async def test_delete_ticket_not_found(client):
    fake_ticket_id = "00000000-0000-0000-0000-000000000000"

    response = await client.delete(
        f"/tickets/{fake_ticket_id}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_ticket_twice(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Delete twice",
            "description": "Testing duplicate deletion",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    first_delete = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert first_delete.status_code == 200

    second_delete = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert second_delete.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ticket_id",
    [
        "invalid-id",
        "123",
        "abc",
        "not-a-uuid",
    ],
)
async def test_delete_ticket_invalid_uuid(client, ticket_id):
    response = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_valid_uuid_not_found(client):
    ticket_id = str(uuid4())

    response = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_only_target_ticket(client):
    first_response = await client.post(
        "/tickets/",
        json={
            "title": "First ticket",
            "description": "This will be deleted",
        },
    )

    second_response = await client.post(
        "/tickets/",
        json={
            "title": "Second ticket",
            "description": "This should remain",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_id = first_response.json()["id"]
    second_id = second_response.json()["id"]

    delete_response = await client.delete(
        f"/tickets/{first_id}"
    )

    assert delete_response.status_code == 200

    first_get = await client.get(
        f"/tickets/{first_id}"
    )

    second_get = await client.get(
        f"/tickets/{second_id}"
    )

    assert first_get.status_code == 404
    assert second_get.status_code == 200


@pytest.mark.asyncio
async def test_delete_ticket_response_message(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Response test",
            "description": "Testing delete response",
        },
    )

    ticket_id = create_response.json()["id"]

    response = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert data["message"] == "Ticket deleted successfully"