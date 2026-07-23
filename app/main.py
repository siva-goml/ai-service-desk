from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.tickets import router as ticket_router
from app.api.ai import router as ai_router
from app.db.database import engine

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from fastapi.responses import JSONResponse
import time

@asynccontextmanager
async def lifespan(app: FastAPI):

    # async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        
    yield

    await engine.dispose()


app = FastAPI(title="AI Service Desk", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

@app.middleware("http")
async def add_response_time(request: Request, call_next,):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2,)
    response.headers["X-Response-Time"] = f"{elapsed_ms}ms"
    return response
 
 
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}
 
@app.get("/ready", tags=["System"])
async def readiness_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
        }
    except Exception:
        return JSONResponse( 
            status_code=503,
            content={
                "status": "not_ready",
                "database": "unavailable",
            },
        )

app.include_router(ticket_router)
app.include_router(ai_router)