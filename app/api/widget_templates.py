from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
import openai
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.schemas.widget_template import (
    GenerateWidgetTemplate,
    WidgetTemplate,
    WidgetTemplateCreate,
    WidgetTemplateUpdate,
)
from app.api import deps
from app.config import settings
from app.models.user import User

router = APIRouter()
client = openai.OpenAI(base_url=settings.OPENAI_API_URL, api_key=settings.OPENAI_API_KEY)

@router.post("/", response_model=WidgetTemplate)
def create_widget_template(
    widget_template: WidgetTemplateCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Check if the user owns the host
    host = crud.host.get(db, id=widget_template.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create widget template for this host",
        )
    return crud.widget_template.create_with_host(
        db=db, obj_in=widget_template, host_id=widget_template.host_id
    )


@router.get("/", response_model=List[WidgetTemplate])
def read_widget_templates(
    skip: int = 0,
    limit: int = 100,
    host_id: UUID = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if host_id:
        # Check if the user owns the host
        host = crud.host.get(db, id=host_id)
        if not host or host.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view widget templates for this host",
            )
        widget_templates = crud.widget_template.get_widget_templates_by_host(
            db, host_id=host_id
        )
    else:
        widget_templates = crud.widget_template.get_multi(db, skip=skip, limit=limit)
    return widget_templates


@router.get("/{widget_template_id}", response_model=WidgetTemplate)
def read_widget_template(
    widget_template_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    widget_template = crud.widget_template.get(db, id=widget_template_id)
    if not widget_template:
        raise HTTPException(status_code=404, detail="Widget template not found")
    # Check if the user owns the host associated with the widget template
    host = crud.host.get(db, id=widget_template.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this widget template"
        )
    return widget_template


@router.put("/{widget_template_id}", response_model=WidgetTemplate)
def update_widget_template(
    widget_template_id: UUID,
    widget_template: WidgetTemplateUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_widget_template = crud.widget_template.get(db, id=widget_template_id)
    if not db_widget_template:
        raise HTTPException(status_code=404, detail="Widget template not found")
    # Check if the user owns the host associated with the widget template
    host = crud.host.get(db, id=db_widget_template.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this widget template"
        )
    return crud.widget_template.update(
        db, db_obj=db_widget_template, obj_in=widget_template
    )


@router.delete("/{widget_template_id}", response_model=WidgetTemplate)
def delete_widget_template(
    widget_template_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    widget_template = crud.widget_template.get(db, id=widget_template_id)
    if not widget_template:
        raise HTTPException(status_code=404, detail="Widget template not found")
    # Check if the user owns the host associated with the widget template
    host = crud.host.get(db, id=widget_template.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this widget template"
        )
    return crud.widget_template.remove(db, id=widget_template_id)


@router.post("/generate_template_with_ai", response_model=GenerateWidgetTemplate)
def generate_template_with_ai(
    prompt: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Call OpenAI API to generate the widget template
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        generated_content = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    return GenerateWidgetTemplate(
        prompt=prompt,
        template=generated_content,
        config={},
    )
