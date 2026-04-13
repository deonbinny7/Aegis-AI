from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_analytics():
    """Get aggregated analytics."""
    return {"status": "implemented in backend"}

@router.get("/usage")
async def get_usage():
    return {"status": "implemented in backend"}

@router.get("/costs")
async def get_costs():
    return {"status": "implemented in backend"}
