from pydantic import UUID4, BaseModel
from typing import Optional


class HostBase(BaseModel):
    name: str


class HostCreate(HostBase):
    pass


class HostUpdate(HostBase):
    name: Optional[str] = None


class Host(HostBase):
    id: UUID4
    owner_id: UUID4

    class Config:
        from_attributes = True
