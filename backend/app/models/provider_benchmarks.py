from sqlalchemy import Column, String, Float, Integer, Boolean
from app.db.base import Base
import uuid

class ProviderBenchmark(Base):
    __tablename__ = "provider_benchmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False, index=True)
    model_name = Column(String, nullable=False, index=True)
    availability_pct = Column(Float, default=100.0)
    avg_latency_ms = Column(Float, default=0.0)
    total_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    throughput_tps = Column(Float, default=0.0)
