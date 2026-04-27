from sqlalchemy import Column, String, Float, Integer
from app.db.base import Base
import uuid

class ProviderPricing(Base):
    __tablename__ = "provider_pricing"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False, index=True)
    model_name = Column(String, nullable=False, index=True)
    input_price_per_token = Column(Float, nullable=False, default=0.0)
    output_price_per_token = Column(Float, nullable=False, default=0.0)
    currency = Column(String, default="USD")
    # For versioned pricing tables
    version = Column(Integer, default=1)
