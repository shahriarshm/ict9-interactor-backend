from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base


class HostUser(Base):
    __tablename__ = "host_users"

    host_id = Column(UUID(as_uuid=True), ForeignKey("hosts.id"), nullable=False)
    client_reference_id = Column(String(255), nullable=True)

    host = relationship("Host", back_populates="host_users")
