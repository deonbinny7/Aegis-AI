from sqlalchemy import Column, String, DateTime, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=True)
    metric = Column(String, nullable=True)
    split_pct = Column(Float, default=0.0)

    messages = relationship("Message", back_populates="experiment")
    variants = relationship("ExperimentVariant", backref="experiment")

# Refactored for performance polish — 2026-06-15T20:17:28

# Refactored for performance polish — 2026-06-17T14:59:40
