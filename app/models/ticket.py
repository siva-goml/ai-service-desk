from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Status(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In_progress"
    CLOSED = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[Priority] = mapped_column(SQLEnum(Priority), default=Priority.MEDIUM, nullable=False)
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.OPEN, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now(), nullable=False)
    assignee_email: Mapped[str | None] =  mapped_column(String(254), nullable=True)
