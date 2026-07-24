import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketUpdate, Priority, Status


def test_update_allows_empty_body():
    update = TicketUpdate()

    assert update.title is None
    assert update.description is None
    assert update.priority is None
    assert update.status is None


def test_update_with_all_fields():
    update = TicketUpdate(
        title="Updated Ticket",
        description="Updated description",
        priority=Priority.HIGH,
        status=Status.IN_PROGRESS,
    )

    assert update.title == "Updated Ticket"
    assert update.description == "Updated description"
    assert update.priority == Priority.HIGH
    assert update.status == Status.IN_PROGRESS


def test_update_only_title():
    update = TicketUpdate(title="New Title")

    assert update.title == "New Title"
    assert update.description is None
    assert update.priority is None
    assert update.status is None


def test_update_only_description():
    update = TicketUpdate(description="New Description")

    assert update.title is None
    assert update.description == "New Description"
    assert update.priority is None
    assert update.status is None


def test_update_only_priority():
    update = TicketUpdate(priority=Priority.HIGH)

    assert update.title is None
    assert update.description is None
    assert update.priority == Priority.HIGH
    assert update.status is None


def test_update_only_status():
    update = TicketUpdate(status=Status.CLOSED)

    assert update.title is None
    assert update.description is None
    assert update.priority is None
    assert update.status == Status.CLOSED


def test_update_multiple_fields():
    update = TicketUpdate(
        title="New Title",
        priority=Priority.LOW,
    )

    assert update.title == "New Title"
    assert update.priority == Priority.LOW
    assert update.description is None
    assert update.status is None



def test_all_valid_priorities():
    for priority in ["High", "Medium", "Low"]:
        update = TicketUpdate(priority=priority)

        assert update.priority.value == priority


def test_all_valid_statuses():
    for status in ["Open", "In_progress", "Closed"]:
        update = TicketUpdate(status=status)

        assert update.status.value == status



def test_invalid_priority():
    with pytest.raises(ValidationError):
        TicketUpdate(priority="Urgent")


def test_invalid_status():
    with pytest.raises(ValidationError):
        TicketUpdate(status="Pending")


def test_invalid_priority_case_sensitive():
    with pytest.raises(ValidationError):
        TicketUpdate(priority="high")


def test_invalid_status_case_sensitive():
    with pytest.raises(ValidationError):
        TicketUpdate(status="open")


def test_invalid_priority_empty_string():
    with pytest.raises(ValidationError):
        TicketUpdate(priority="")


def test_invalid_status_empty_string():
    with pytest.raises(ValidationError):
        TicketUpdate(status="")



def test_update_with_explicit_none():
    update = TicketUpdate(
        title=None,
        description=None,
        priority=None,
        status=None,
    )

    assert update.title is None
    assert update.description is None
    assert update.priority is None
    assert update.status is None


def test_update_with_empty_strings_for_text_fields():
    update = TicketUpdate(
        title="",
        description="",
    )

    assert update.title == ""
    assert update.description == ""


def test_update_with_whitespace():
    update = TicketUpdate(
        title="   ",
        description="   ",
    )

    assert update.title == "   "
    assert update.description == "   "


def test_update_with_long_title():
    long_title = "A" * 1000

    update = TicketUpdate(title=long_title)

    assert update.title == long_title


def test_update_with_long_description():
    long_description = "A" * 5000

    update = TicketUpdate(description=long_description)

    assert update.description == long_description


def test_update_with_special_characters():
    update = TicketUpdate(
        title="Ticket @#$%^&*",
        description="Error: API failed! <500>",
    )

    assert update.title == "Ticket @#$%^&*"
    assert update.description == "Error: API failed! <500>"




def test_invalid_priority_type():
    with pytest.raises(ValidationError):
        TicketUpdate(priority=123)


def test_invalid_status_type():
    with pytest.raises(ValidationError):
        TicketUpdate(status=123)