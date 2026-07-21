from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.tickets import router as ticket_router
from app.db.base import Base
from app.db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(title="AI Service Desk", lifespan=lifespan)

app.include_router(ticket_router)
