from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base


class Host(Base):
    __tablename__ = "hosts"

    name = Column(String, nullable=False)
    api_key = Column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    owner = relationship("User", back_populates="host")
    campaigns = relationship("Campaign", back_populates="host")
    widget_templates = relationship("WidgetTemplate", back_populates="host")
    widgets = relationship("Widget", back_populates="host")

    host_users = relationship("HostUser", back_populates="host")
