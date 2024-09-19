from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud
from app.models.campaign import CampaignStatus
from app.schemas.widget import Widget, WidgetCreate, WidgetUpdate
from app.api import deps
from app.models.user import User
from app.services.widget_service import widget_service
from app.utils import add_default_js_to_html

router = APIRouter()


@router.post("/", response_model=Widget)
def create_widget(
    widget: WidgetCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    template = crud.widget_template.get(db, id=widget.widget_template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Widget template not found")

    campaign = crud.campaign.get(db, id=widget.campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign.status != CampaignStatus.active:
        raise HTTPException(
            status_code=400, detail="Cannot create widget for inactive campaign"
        )

    template.template = add_default_js_to_html(template.template)

    obj = crud.widget.create_with_template(db=db, obj_in=widget, template=template)

    widget_data = {
        "widget_id": obj.id,
        "host_id": obj.host_id,
        "campaign_id": obj.campaign_id,
        "body": obj.body,
        "config": obj.config,
    }
    widget_service.create_widget(widget_data)
    return obj


@router.get("/", response_model=List[Widget])
def read_widgets(
    skip: int = 0,
    limit: int = 100,
    campaign_id: Optional[UUID] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if campaign_id:
        widgets = crud.widget.get_multi_by_campaign(
            db, skip=skip, limit=limit, campaign_id=campaign_id
        )
    else:
        widgets = crud.widget.get_multi(db, skip=skip, limit=limit)
    return widgets


@router.get("/{widget_id}", response_model=Widget)
def read_widget(
    widget_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_widget = crud.widget.get(db, id=widget_id)
    if db_widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")
    return db_widget


@router.put("/{widget_id}", response_model=Widget)
def update_widget(
    widget_id: UUID,
    widget: WidgetUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_widget = crud.widget.get(db, id=widget_id)
    if db_widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")
    obj = crud.widget.update(db, db_obj=db_widget, obj_in=widget)

    widget_data = {
        "host_id": obj.host_id,
        "campaign_id": obj.campaign_id,
        "body": obj.body,
        "config": obj.config,
    }
    widget_service.update_widget(obj.id, widget_data)
    return obj


@router.delete("/{widget_id}", response_model=Widget)
def delete_widget(
    widget_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_widget = crud.widget.get(db, id=widget_id)
    if db_widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")
    obj = crud.widget.remove(db, id=widget_id)
    widget_service.delete_widget(obj.id)
    return obj
