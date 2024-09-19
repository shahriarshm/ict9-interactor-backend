from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.discount_code import DiscountCode
from app.schemas.discount_code import DiscountCodeCreate, DiscountCodeUpdate


class CRUDDiscountCode(CRUDBase[DiscountCode, DiscountCodeCreate, DiscountCodeUpdate]):
    def create_with_campaign(
        self, db: Session, *, obj_in: DiscountCodeCreate, campaign_id: UUID
    ) -> DiscountCode:
        db_obj = DiscountCode(
            code=obj_in.code,
            discount_value=obj_in.discount_value,
            discount_type=obj_in.discount_type,
            max_uses=obj_in.max_uses,
            expiration_date=obj_in.expiration_date,
            is_active=obj_in.is_active,
            campaign_id=campaign_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_discount_codes_by_campaign(self, db: Session, campaign_id: UUID):
        return (
            db.query(DiscountCode).filter(DiscountCode.campaign_id == campaign_id).all()
        )


discount_code = CRUDDiscountCode(DiscountCode)
