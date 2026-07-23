from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import Priority, Status


class TicketCreate(BaseModel):
    model_config = ConfigDict(
       str_strip_whitespace=True
    )
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    priority: Priority = Priority.MEDIUM
    assignee_email: Optional[str] = None


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None

class TicketResponse(BaseModel):
    id: UUID
    title: str
    description: str
    priority: Priority
    assignee_email: Optional[str] = None
    status: Status
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str
