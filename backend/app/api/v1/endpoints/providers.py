from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_providers():
    return {"status": "implemented in backend"}
