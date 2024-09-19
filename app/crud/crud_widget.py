from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.widget import Widget
from app.models.widget_template import WidgetTemplate
from app.schemas.widget import WidgetCreate, WidgetUpdate
from typing import List, Optional
from uuid import UUID

class CRUDWidget(CRUDBase[Widget, WidgetCreate, WidgetUpdate]):
    def create_with_template(
        self, db: Session, *, obj_in: WidgetCreate, template: WidgetTemplate
    ) -> Widget:
        db_obj = self.model(
            **obj_in.model_dump(),
            body=template.template,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_campaign(
        self, db: Session, *, skip: int = 0, limit: int = 100, campaign_id: Optional[UUID] = None
    ) -> List[Widget]:
        query = db.query(self.model).filter(self.model.campaign_id == campaign_id)
        return query.offset(skip).limit(limit).all()

widget = CRUDWidget(Widget)
