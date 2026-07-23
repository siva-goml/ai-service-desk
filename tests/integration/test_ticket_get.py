import pytest

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

@pytest.mark.asyncio
async def test_get_ticket_not_found(client):

    fake_ticket_id = "00000000-0000-0000-0000-000000000000"

    response = await client.get(
        f"/tickets/{fake_ticket_id}"
    )
    assert response.status_code == 404