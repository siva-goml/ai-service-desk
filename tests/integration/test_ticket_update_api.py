import pytest
from uuid import uuid4


@pytest.mark.asyncio
async def test_update_ticket(client):

    create_payload = {
        "title": "Original title",
        "description": "Original description",
        "priority": "Medium",
    }

    create_response = await client.post(
        "/tickets/",
        json=create_payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    update_payload = {
        "title": "Updated title",
        "priority": "High",
    }

    response = await client.put(
        f"/tickets/{ticket_id}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket_id
    assert data["title"] == "Updated title"
    assert data["priority"] == "High"
    assert data["description"] == "Original description"


@pytest.mark.asyncio
async def test_update_ticket_not_found(client):

    fake_ticket_id = "00000000-0000-0000-0000-000000000000"

    payload = {
        "title": "Updated title",
    }

    response = await client.put(
        f"/tickets/{fake_ticket_id}",
        json=payload,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_ticket_only_title(client):

    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Original title",
            "description": "Original description",
            "priority": "Medium",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={
            "title": "Updated title",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["description"] == "Original description"
    assert data["priority"] == "Medium"


@pytest.mark.asyncio
async def test_update_ticket_only_description(client):

    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Original title",
            "description": "Original description",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={
            "description": "Updated description",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Original title"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_update_ticket_priority(client):

    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Priority test",
            "description": "Testing priority update",
            "priority": "Low",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": "High",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["priority"] == "High"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "priority",
    [
        "Urgent",
        "Critical",
        "high",
        "medium",
        "low",
        "",
    ],
)
async def test_update_ticket_invalid_priority(client, priority):

    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Priority test",
            "description": "Testing invalid priority",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": priority,
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_ticket_invalid_uuid(client):

    response = await client.put(
        "/tickets/invalid-id",
        json={
            "title": "Updated title",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_ticket_random_uuid_not_found(client):

    fake_ticket_id = str(uuid4())

    response = await client.put(
        f"/tickets/{fake_ticket_id}",
        json={
            "title": "Updated title",
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_empty_body(client):

    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Original title",
            "description": "Original description",
            "priority": "Medium",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.put(
        f"/tickets/{ticket_id}",
        json={},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Original title"
    assert data["description"] == "Original description"
    assert data["priority"] == "Medium"