from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.widget_template import WidgetTemplate
from app.schemas.widget_template import WidgetTemplateCreate, WidgetTemplateUpdate


class CRUDWidgetTemplate(
    CRUDBase[WidgetTemplate, WidgetTemplateCreate, WidgetTemplateUpdate]
):
    def create_with_host(
        self, db: Session, *, obj_in: WidgetTemplateCreate, host_id: UUID
    ) -> WidgetTemplate:
        db_obj = WidgetTemplate(
            name=obj_in.name,
            description=obj_in.description,
            type=obj_in.type,
            template=obj_in.template,
            host_id=host_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_widget_templates_by_host(self, db: Session, host_id: UUID):
        return db.query(WidgetTemplate).filter(WidgetTemplate.host_id == host_id).all()


widget_template = CRUDWidgetTemplate(WidgetTemplate)
