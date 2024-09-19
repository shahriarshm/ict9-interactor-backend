from sqlalchemy import Column, String, ForeignKey, Date, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import enum


class CampaignStatus(enum.Enum):
    draft = "draft"
    active = "active"
    expired = "expired"


class CampaignType(enum.Enum):
    email = "email"
    social_media = "social_media"
    display_ads = "display_ads"
    content_marketing = "content_marketing"
    event = "event"


class Campaign(Base):
    __tablename__ = "campaigns"

    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(CampaignStatus), nullable=False, default=CampaignStatus.draft)
    type = Column(Enum(CampaignType), nullable=False)

    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    host_id = Column(UUID(as_uuid=True), ForeignKey("hosts.id"), nullable=False)

    creator = relationship("User", back_populates="campaigns")
    host = relationship("Host", back_populates="campaigns")
    widgets = relationship("Widget", back_populates="campaign")
    discount_codes = relationship("DiscountCode", back_populates="campaign")
