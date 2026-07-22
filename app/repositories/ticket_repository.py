from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, db_ticket: Ticket):
        self.db.add(db_ticket)
        await self.db.flush()
        await self.db.refresh(db_ticket)
        return db_ticket

    async def get_all(self):
        result = await self.db.execute(select(Ticket).order_by(Ticket.created_at.desc()))
        return list(result.scalars().all())

    async def get(self, ticket_id: UUID):
        return await self.db.get(Ticket, ticket_id)

    async def update(self, db_ticket: Ticket):
        await self.db.flush()
        await self.db.refresh(db_ticket)
        return db_ticket
        
    async def delete(self, ticket_id: UUID) -> Ticket | None:
        db_ticket = await self.get(ticket_id)
        if db_ticket is None:
            return None
        await self.db.delete(db_ticket)
        await self.db.flush()
        return db_ticket
