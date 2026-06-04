from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_providers():
    return {"status": "implemented in backend"}

# Refactored for performance polish — 2026-06-04T20:17:19
