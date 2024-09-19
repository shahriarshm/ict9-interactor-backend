from pydantic import UUID4, BaseModel, constr
from typing import Optional
from enum import Enum

from app.models.widget_template import WidgetType


class WidgetTemplateBase(BaseModel):
    name: constr(max_length=255)
    description: Optional[str] = None
    type: WidgetType
    template: str
    config: dict
    host_id: UUID4


class WidgetTemplateCreate(WidgetTemplateBase):
    pass


class WidgetTemplateUpdate(BaseModel):
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    type: Optional[WidgetType] = None
    template: Optional[str] = None
    config: Optional[dict] = None
    host_id: Optional[UUID4] = None


class WidgetTemplate(WidgetTemplateBase):
    id: UUID4

    class Config:
        from_attributes = True


class GenerateWidgetTemplate(BaseModel):
    prompt: str
    template: str
    config: dict = {}