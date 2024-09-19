from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.host_user import HostUser, HostUserUpdate
from app.api.deps import get_db

router = APIRouter()


@router.get("/{host_user_id}", response_model=HostUser)
def read_host_user(host_user_id: UUID, db: Session = Depends(get_db)):
    db_host_user = crud.host_user.get_host_user(db, host_user_id)
    if db_host_user is None:
        raise HTTPException(status_code=404, detail="Host user not found")
    return db_host_user


@router.put("/{host_user_id}", response_model=HostUser)
def update_host_user(
    host_user_id: UUID, host_user: HostUserUpdate, db: Session = Depends(get_db)
):
    db_host_user = crud.host_user.update_host_user(db, host_user_id, host_user)
    if db_host_user is None:
        raise HTTPException(status_code=404, detail="Host user not found")
    return db_host_user


@router.delete("/{host_user_id}", response_model=HostUser)
def delete_host_user(host_user_id: UUID, db: Session = Depends(get_db)):
    db_host_user = crud.host_user.delete_host_user(db, host_user_id)
    if db_host_user is None:
        raise HTTPException(status_code=404, detail="Host user not found")
    return db_host_user
