from sqlalchemy import Column, String, Integer, JSON
from app.db.base import Base
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True, index=True)
    provider = Column(String, nullable=True)
    prompt_version_id = Column(String, nullable=True)
    experiment_id = Column(String, nullable=True)
    session_id = Column(String, nullable=True, index=True)
    status = Column(String, nullable=False, default="success")
    retry_count = Column(Integer, default=0)
    
    metadata_ = Column("metadata", JSON, default={})
