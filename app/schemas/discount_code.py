from pydantic import UUID4, BaseModel, constr
from typing import Optional
from datetime import date
from enum import Enum
from decimal import Decimal


class DiscountType(str, Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"
    free_shipping = "free_shipping"


class DiscountCodeBase(BaseModel):
    code: constr(max_length=50)
    discount_value: Decimal
    discount_type: DiscountType
    max_uses: Optional[int] = None
    expiration_date: Optional[date] = None
    is_active: bool = True
    campaign_id: UUID4


class DiscountCodeCreate(DiscountCodeBase):
    pass


class DiscountCodeUpdate(BaseModel):
    discount_value: Optional[Decimal] = None
    discount_type: Optional[DiscountType] = None
    max_uses: Optional[int] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None


class DiscountCode(DiscountCodeBase):
    id: UUID4
    host_id: UUID4

    class Config:
        from_attributes = True
