from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"

@router.get("", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")

@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    # In a real app, check DB and Redis connections here
    return HealthResponse(status="ready")

@router.get("/live", response_model=HealthResponse)
async def liveness_check():
    return HealthResponse(status="alive")
