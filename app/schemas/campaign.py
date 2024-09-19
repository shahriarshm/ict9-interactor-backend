from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date
from enum import Enum


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class CampaignType(str, Enum):
    email = "email"
    social_media = "social_media"
    display_ads = "display_ads"
    content_marketing = "content_marketing"
    event = "event"


class CampaignBase(BaseModel):
    name: str
    host_id: UUID4
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: CampaignStatus
    type: CampaignType


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CampaignStatus] = None
    type: Optional[CampaignType] = None


class Campaign(CampaignBase):
    id: UUID4
    creator_id: UUID4
    host_id: UUID4

    class Config:
        from_attributes = True
