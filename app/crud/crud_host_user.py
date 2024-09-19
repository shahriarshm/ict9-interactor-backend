from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.host_user import HostUser
from app.schemas.host_user import HostUserCreate, HostUserUpdate


class CRUDHostUser(CRUDBase[HostUser, HostUserCreate, HostUserUpdate]):
    def get_or_create_by_client_ref_id(self, db: Session, client_reference_id: str):
        db_host_user = (
            db.query(HostUser)
            .filter(HostUser.client_reference_id == client_reference_id)
            .first()
        )
        if db_host_user is None:
            db_host_user = HostUser(client_reference_id=client_reference_id)
            db.add(db_host_user)
            db.commit()
            db.refresh(db_host_user)
        return db_host_user


host_user = CRUDHostUser(HostUser)
