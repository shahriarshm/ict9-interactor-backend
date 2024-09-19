from sqlalchemy import Column, String, ForeignKey, Date, Enum, Integer, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import enum


class DiscountType(enum.Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"
    free_shipping = "free_shipping"


class DiscountCode(Base):
    __tablename__ = "discount_codes"

    code = Column(String(50), nullable=False, unique=True)
    discount_value = Column(Numeric(10, 2), nullable=False)
    discount_type = Column(Enum(DiscountType), nullable=False)
    max_uses = Column(Integer, nullable=True)
    current_uses = Column(Integer, default=0, nullable=False)
    expiration_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    campaign = relationship("Campaign", back_populates="discount_codes")
