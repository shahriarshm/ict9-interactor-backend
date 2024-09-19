from sqlalchemy import JSON, Column, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum
from sqlalchemy.dialects.postgresql import UUID


class WidgetType(enum.Enum):
    game = "game"
    survey = "survey"
    quiz = "quiz"
    form = "form"
    calculator = "calculator"


class WidgetTemplate(Base):
    __tablename__ = "widget_templates"

    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(Enum(WidgetType), nullable=False)
    template = Column(Text, nullable=False)
    config = Column(JSON, nullable=False)
    host_id = Column(UUID(as_uuid=True), ForeignKey("hosts.id"), nullable=False)

    host = relationship("Host", back_populates="widget_templates")
    widgets = relationship("Widget", back_populates="widget_template")
