from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
import openai
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, utils
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
client = openai.OpenAI(
    base_url=settings.OPENAI_API_URL, api_key=settings.OPENAI_API_KEY
)


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


    # Check if the widget template is safe
    is_safe, reason = utils.is_html_safe(widget_template.template)
    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail=f"Widget template is not safe: {reason}",
        )

    return crud.widget_template.create_with_host(
        db=db, obj_in=widget_template, host_id=widget_template.host_id
    )


@router.get("/", response_model=List[WidgetTemplate])
def read_widget_templates(
    skip: int = 0,
    limit: int = 100,
    host_id: Optional[UUID] = None,
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
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert HTML developer specializing in creating interactive, compact, and user-friendly campaign widgets such as small games, banners, and forms. Your goal is to generate HTML that maximizes user engagement. IMPORTANT: Only return the HTML content, without any explanations or additional text."},
                {"role": "user", "content": f"Create a compact, interactive HTML widget for a campaign based on this prompt: {prompt}. The widget should be engaging, user-friendly, and designed to increase user interaction. Include any necessary inline CSS and JavaScript to make the widget self-contained and easily embeddable. IMPORTANT: Only provide the HTML content, nothing else."},
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        generated_content = response.choices[0].message.content
        generated_content = generated_content.replace("```html", "").replace("```", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    return GenerateWidgetTemplate(
        prompt=prompt,
        template=generated_content,
        config={},
    )
