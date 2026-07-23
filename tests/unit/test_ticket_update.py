from app.schemas.ticket import TicketUpdate
def test_update_allows_empty_body():
    update = TicketUpdate()

    assert update.title is None
    assert update.description is None
    assert update.priority is None
    assert update.status is None