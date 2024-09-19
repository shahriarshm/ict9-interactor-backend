from pydantic import BaseModel, UUID4
from typing import Optional


class HostUserBase(BaseModel):
    client_reference_id: Optional[str] = None


class HostUserCreate(HostUserBase):
    host_id: UUID4


class HostUserUpdate(HostUserBase):
    pass


class HostUser(HostUserBase):
    id: UUID4
    host_id: UUID4

    class Config:
        from_attributes = True
