from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

class AuditableBase:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
        
    @declared_attr
    def version_id(cls):
        return Column(Integer, default=1, nullable=False)

    @declared_attr
    def __mapper_args__(cls):
        return {"version_id_col": cls.version_id}

Base = declarative_base(cls=AuditableBase)
