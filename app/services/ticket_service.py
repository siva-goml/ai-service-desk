from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, Status
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate

class TicketNotFoundError(Exception):
    pass


class ClosedTicketError(Exception):
    pass


class TicketService:
    def __init__(self, db: AsyncSession):
        self.repository = TicketRepository(db)

    async def create_ticket(self, ticket: TicketCreate):
        ticket = Ticket(**ticket.model_dump())
        return await self.repository.create(ticket)

    async def get_all_ticket(self):
        return await self.repository.get_all()

    async def get_ticket(self, ticket_id: UUID):
        return await self.repository.get(ticket_id)

    async def update_ticket(self, ticket_id: UUID, ticket: TicketUpdate):
        exist_ticket = await self.repository.get(ticket_id)
        if exist_ticket is None:
            raise TicketNotFoundError("Ticket not found")
        if exist_ticket.status == Status.CLOSED:
            raise ClosedTicketError("Closed tickets cannot be updated")
        update_data = ticket.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exist_ticket, field, value)

        return await self.repository.update(exist_ticket)

    async def delete_ticket(self, ticket_id: UUID):
        exist_ticket = await self.repository.get(ticket_id)
        if exist_ticket is None:
            raise TicketNotFoundError("Ticket not found")
        return await self.repository.delete(ticket_id)
