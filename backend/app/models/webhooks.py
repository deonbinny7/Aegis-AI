from sqlalchemy import Column, String, Boolean
from app.db.base import Base
import uuid

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    trigger_event = Column(String, nullable=False, index=True) # e.g. "provider_failure", "high_cost"
    is_active = Column(Boolean, default=True)
