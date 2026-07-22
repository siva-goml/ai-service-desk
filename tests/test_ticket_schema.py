import pytest
def test_create_ticket_with_empty_title_returns_422(client):
    response = client.post(
        "/tickets",
        json={
            "title": "",
        }
    )
    with pytest.raises(KeyError):
        response.json()
 