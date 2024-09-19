from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from typing import List, Tuple, Any

class CRUDCampaign(CRUDBase[Campaign, CampaignCreate, CampaignUpdate]):
    def create_with_user_and_host(
        self, db: Session, *, obj_in: CampaignCreate, user_id: UUID, host_id: UUID
    ) -> Campaign:
        db_obj = Campaign(
            name=obj_in.name,
            creator_id=user_id,
            host_id=host_id,
            description=obj_in.description,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            status=obj_in.status,
            type=obj_in.type,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_with_filters(
        self, db: Session, *, skip: int = 0, limit: int = 100, filters: List[Tuple[str, Any]] = []
    ) -> List[Campaign]:
        query = db.query(self.model)
        for field, value in filters:
            query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

campaign = CRUDCampaign(Campaign)
