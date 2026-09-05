"""FastAPI-applikationen för Dataview.

Startpunkt för backend. Kör lokalt med:

    uvicorn backend.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.db.database import init_db
from backend.schemas.common import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Skapar databastabellerna innan appen börjar ta emot anrop."""
    init_db()
    yield


app = FastAPI(
    title="Dataview API",
    description="Ladda upp en CSV, välj target och få tre jämförda scikit-learn-modeller.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Enkel livskontroll som frontend använder för att se att backend svarar."""
    return HealthResponse(status="ok", version=app.version)
