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
    data = response.json()
    assert data["priority"] == "Medium"

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
async def test_create_ticket_invalid_payload(client,payload):
    response = await client.post(
        "/tickets/",
        json=payload,
    )
    assert response.status_code == 422