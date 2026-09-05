"""Scheman som delas av flera endpoints."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Svar från GET /health."""

    status: str
    version: str
