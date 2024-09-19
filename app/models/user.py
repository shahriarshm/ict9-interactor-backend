from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    host = relationship("Host", back_populates="owner", uselist=False)
    campaigns = relationship("Campaign", back_populates="creator")
