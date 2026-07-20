from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    title:str
    description:str
    priority:str = "Medium"

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class Ticket(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    
