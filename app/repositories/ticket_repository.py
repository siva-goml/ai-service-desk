from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, ticket: TicketCreate):
        db_ticket = Ticket(**ticket.model_dump())
        self.db.add(db_ticket)
        try:
            await self.db.commit()
            await self.db.refresh(db_ticket)
            return db_ticket
        except Exception:
            await self.db.rollback()
            raise

    async def get_all(self):
        result = await self.db.execute(select(Ticket).order_by(Ticket.created_at.desc()))
        return list(result.scalars().all())

    async def get(self, ticket_id: UUID):
        return await self.db.get(Ticket, ticket_id)

    async def update(self, ticket_id: UUID, ticket: TicketUpdate):
        db_ticket = await self.get(ticket_id)
        if db_ticket is None:
            return None
        for field, value in ticket.model_dump(exclude_unset=True).items():
            setattr(db_ticket, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_ticket)
            return db_ticket
        except Exception:
            await self.db.rollback()
            raise
        
    async def delete(self, ticket_id: UUID) -> Ticket | None:
        db_ticket = await self.get(ticket_id)
        if db_ticket is None:
            return None
        await self.db.delete(db_ticket)
        try:
            await self.db.commit()
            return db_ticket
        except Exception:
            await self.db.rollback()
            raise
