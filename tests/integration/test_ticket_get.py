import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_ticket(client):
    create_payload = {
        "title": "Login issue",
        "description": "Login failed",
        "priority": "High",
    }

    create_response = await client.post(
        "/tickets/",
        json=create_payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket_id
    assert data["title"] == "Login issue"
    assert data["description"] == "Login failed"
    assert data["priority"] == "High"


@pytest.mark.asyncio
async def test_get_ticket_not_found(client):
    fake_ticket_id = "00000000-0000-0000-0000-000000000000"

    response = await client.get(
        f"/tickets/{fake_ticket_id}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_ticket_random_uuid_not_found(client):
    fake_ticket_id = str(uuid4())

    response = await client.get(
        f"/tickets/{fake_ticket_id}"
    )

    assert response.status_code == 404


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
async def test_get_ticket_invalid_uuid(client, ticket_id):
    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_ticket_with_all_fields(client):
    create_payload = {
        "title": "Database issue",
        "description": "Database connection failed",
        "priority": "High",
        "assignee_email": "admin@example.com",
    }

    create_response = await client.post(
        "/tickets/",
        json=create_payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Database issue"
    assert data["description"] == "Database connection failed"
    assert data["priority"] == "High"
    assert data["assignee_email"] == "admin@example.com"


@pytest.mark.asyncio
async def test_get_ticket_default_priority(client):
    create_payload = {
        "title": "Default priority",
        "description": "Testing default priority",
    }

    create_response = await client.post(
        "/tickets/",
        json=create_payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["priority"] == "Medium"


@pytest.mark.asyncio
async def test_get_ticket_after_delete(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Ticket to delete",
            "description": "This will be deleted",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    delete_response = await client.delete(
        f"/tickets/{ticket_id}"
    )

    assert delete_response.status_code == 200

    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_multiple_tickets_independently(client):
    first_response = await client.post(
        "/tickets/",
        json={
            "title": "First ticket",
            "description": "First description",
        },
    )

    second_response = await client.post(
        "/tickets/",
        json={
            "title": "Second ticket",
            "description": "Second description",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_id = first_response.json()["id"]
    second_id = second_response.json()["id"]

    first_get = await client.get(
        f"/tickets/{first_id}"
    )

    second_get = await client.get(
        f"/tickets/{second_id}"
    )

    assert first_get.status_code == 200
    assert second_get.status_code == 200

    assert first_get.json()["title"] == "First ticket"
    assert second_get.json()["title"] == "Second ticket"


@pytest.mark.asyncio
async def test_get_ticket_response_structure(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Response test",
            "description": "Testing response structure",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(
        f"/tickets/{ticket_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "priority" in data
    assert "assignee_email" in data