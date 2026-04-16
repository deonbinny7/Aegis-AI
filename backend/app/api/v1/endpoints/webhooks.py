from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class WebhookCreate(BaseModel):
    url: str
    trigger_event: str

@router.post("")
async def create_webhook(webhook: WebhookCreate):
    return {"status": "created", "url": webhook.url}
