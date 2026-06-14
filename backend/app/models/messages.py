from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    prompt_version_id = Column(String, ForeignKey("prompt_versions.id", ondelete="SET NULL"), nullable=True)
    experiment_id = Column(String, ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True)
    role = Column(String, nullable=False) # e.g. "user", "assistant", "system"
    content = Column(String, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)

    session = relationship("Session", back_populates="messages")
    prompt_version = relationship("PromptVersion", back_populates="messages")
    experiment = relationship("Experiment", back_populates="messages")

# Refactored for performance polish — 2026-06-14T12:55:58
