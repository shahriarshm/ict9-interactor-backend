from pydantic import UUID4, BaseModel, constr, Json
from typing import Optional


class WidgetBase(BaseModel):
    name: constr(max_length=255)
    description: Optional[str] = None
    config: dict


class WidgetCreate(WidgetBase):
    host_id: UUID4
    campaign_id: UUID4
    widget_template_id: UUID4


class WidgetUpdate(BaseModel):
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    config: Optional[dict] = None


class Widget(WidgetBase):
    id: UUID4
    host_id: UUID4
    widget_template_id: UUID4

    class Config:
        from_attributes = True
