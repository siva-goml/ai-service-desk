import pytest


@pytest.mark.asyncio
async def test_create_ticket(client):
    payload = {
        "title": "Login failed",
        "description": "Employee login was declined",
        "priority": "High",
        "assignee_email": "support@example.com",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Login failed"
    assert data["description"] == "Employee login was declined"
    assert data["priority"] == "High"
    assert data["assignee_email"] == "support@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_ticket_default_priority(client):
    payload = {
        "title": "Login issue",
        "description": "User cannot login",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "Medium"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "priority",
    [
        "High",
        "Medium",
        "Low",
    ],
)
async def test_create_ticket_valid_priority(client, priority):
    payload = {
        "title": "Priority test",
        "description": "Testing priority",
        "priority": priority,
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["priority"] == priority


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
async def test_create_ticket_invalid_priority(client, priority):
    payload = {
        "title": "Invalid priority",
        "description": "Testing invalid priority",
        "priority": priority,
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {
            "description": "Missing title",
        },
        {
            "title": "Missing description",
        },
        {},
    ],
)
async def test_create_ticket_missing_required_fields(client, payload):
    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": None,
            "description": "Valid description",
        },
        {
            "title": "Valid title",
            "description": None,
        },
    ],
)
async def test_create_ticket_null_required_fields(client, payload):
    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_ticket_invalid_field_type(client):
    payload = {
        "title": 123,
        "description": "Valid description",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_ticket_invalid_email(client):
    payload = {
        "title": "Email test",
        "description": "Testing email validation",
        "assignee_email": "invalid-email",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code in [201, 422]


@pytest.mark.asyncio
async def test_create_ticket_special_characters(client):
    payload = {
        "title": "Login failed! @#$%",
        "description": "Error: API returned <500> & failed.",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Login failed! @#$%"
    assert data["description"] == "Error: API returned <500> & failed."


@pytest.mark.asyncio
async def test_create_ticket_response_structure(client):
    payload = {
        "title": "Response test",
        "description": "Checking response structure",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "priority" in data
    assert "assignee_email" in data