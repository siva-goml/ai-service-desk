from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    def __init__(self, db: AsyncSession):
        self.repository = TicketRepository(db)

    async def create_ticket(self, ticket: TicketCreate):
        return await self.repository.create(ticket)

    async def get_all_ticket(self):
        return await self.repository.get_all()

    async def get_ticket(self, ticket_id: UUID):
        return await self.repository.get(ticket_id)

    async def update_ticket(self, ticket_id: UUID, ticket: TicketUpdate):
        return await self.repository.update(ticket_id, ticket)

    async def delete_ticket(self, ticket_id: UUID):
        return await self.repository.delete(ticket_id)
