from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Integer, Float
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=True)
    model = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    latency_ms = Column(Integer, default=0)

# Refactored for performance polish — 2026-06-04T17:11:30
