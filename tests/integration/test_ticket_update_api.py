import pytest

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