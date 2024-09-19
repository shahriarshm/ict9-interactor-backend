from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.host import Host
from app.models.user import User
from app.schemas.host import HostCreate, HostUpdate


class CRUDHost(CRUDBase[Host, HostCreate, HostUpdate]):
    def create_with_user(self, db: Session, *, obj_in: HostCreate, user: User) -> Host:
        db_obj = Host(**obj_in.dict(), owner_id=user.id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_default_with_user(self, db: Session, *, user: User) -> Host:
        return db.query(Host).filter(Host.owner_id == user.id).first()


host = CRUDHost(Host)
