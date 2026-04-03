from sqlalchemy import Column, String, ForeignKey, JSON
from app.db.base import Base
import uuid

class ExperimentVariant(Base):
    __tablename__ = "experiment_variants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String, ForeignKey("experiments.id"), nullable=False)
    name = Column(String, nullable=False)
    config = Column(JSON, default={}) # Stores model overrides, prompt versions etc
