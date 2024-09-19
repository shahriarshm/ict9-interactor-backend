from sqlalchemy import JSON, Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.widget_template import WidgetTemplate


class Widget(Base):
    __tablename__ = "widgets"

    host_id = Column(UUID(as_uuid=True), ForeignKey("hosts.id"))
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    body = Column(Text, nullable=False)
    config = Column(JSON, nullable=False)
    widget_template_id = Column(UUID(as_uuid=True), ForeignKey("widget_templates.id"))

    host = relationship("Host", back_populates="widgets")
    campaign = relationship("Campaign", back_populates="widgets")
    widget_template = relationship("WidgetTemplate", back_populates="widgets")
