from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.ticket import TicketResponse, TicketCreate, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    return await TicketService(db).create_ticket(ticket)


@router.get("/", response_model=list[TicketResponse])
async def get_all_tickets(db: AsyncSession = Depends(get_db)):
    return await TicketService(db).get_all_ticket()


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    ticket = await TicketService(db).get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: UUID, ticket: TicketUpdate, db: AsyncSession = Depends(get_db)):
    updated = await TicketService(db).update_ticket(ticket_id, ticket)
    if updated is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated


@router.delete("/{ticket_id}", status_code=status.HTTP_200_OK)
async def delete(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    remove = await TicketService(db).delete_ticket(ticket_id)
    if remove is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
