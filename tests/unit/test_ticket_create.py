import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketCreate

def test_valid_title_works():
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
    )

    assert ticket.title == "Login issue"


@pytest.mark.parametrize(
    "bad_title",
    ["", "   ", "x" * 201,],
)

def test_bad_titles_are_rejected(bad_title):
    with pytest.raises(ValidationError):
        TicketCreate(
            title=bad_title,
            description="Valid description",
        )

def test_title_spaces_are_trimmed():
    ticket = TicketCreate(
        title="  Login issue  ",
        description="Valid description",
    )

    assert ticket.title == "Login issue"




def test_valid_description_works():
    # HAPPY
    ticket = TicketCreate(
        title="Login issue",
        description="Password was rejected",
    )

    assert ticket.description == "Password was rejected"

@pytest.mark.parametrize(
    "bad_description",
    [
        "",           
        "   ",        
        "x" * 5001,  
    ],
)
def test_bad_descriptions_are_rejected(bad_description):
    with pytest.raises(ValidationError):
        TicketCreate(
            title="Login issue",
            description=bad_description,
        )

def test_description_spaces_are_trimmed():
    # EDGE
    ticket = TicketCreate(
        title="Login issue",
        description="  Password rejected  ",
    )

    assert ticket.description == "Password rejected"


@pytest.mark.parametrize(
    "priority",
    [
        "Low",
        "Medium",
        "High",
    ],
)
def test_valid_priority_values(priority):
    # HAPPY
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
        priority=priority,
    )

    assert ticket.priority == priority


def test_priority_default_is_medium():
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
    )

    assert ticket.priority == "Medium"


@pytest.mark.parametrize(
    "bad_priority",
    [
        "urgent",  
        "HIGH",   
        "",        
        123,  
    ],
)
def test_invalid_priority_values_rejected(bad_priority):
    with pytest.raises(ValidationError):
        TicketCreate(
            title="Login issue",
            description="Password rejected",
            priority=bad_priority,
        )


def test_valid_assignee_email_works():
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
        assignee_email="user@example.com",
    )

    assert ticket.assignee_email == "user@example.com"


def test_assignee_email_can_be_none():
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
        assignee_email=None,
    )

    assert ticket.assignee_email is None


def test_assignee_email_can_be_omitted():
    ticket = TicketCreate(
        title="Login issue",
        description="Password rejected",
    )

    assert ticket.assignee_email is None
