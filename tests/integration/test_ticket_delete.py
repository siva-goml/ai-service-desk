import pytest

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

    get_response = await client.get(
        f"/tickets/{ticket_id}"
    )
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_ticket_not_found(client):

    fake_ticket_id = "00000000-0000-0000-0000-000000000000"

    response = await client.delete(
        f"/tickets/{fake_ticket_id}"
    )

    assert response.status_code == 404