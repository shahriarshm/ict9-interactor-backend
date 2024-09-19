import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.sql import func


class Base:
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=Base)
