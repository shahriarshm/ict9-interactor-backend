from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.host import Host, HostCreate, HostUpdate
from app.api.deps import get_current_user, get_db
from app.schemas.user import User

router = APIRouter()


@router.post("/", response_model=Host)
def create_host(
    host: HostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.host.create_with_user(db, obj_in=host, user=current_user)


@router.get("/default", response_model=Host)
def read_default_host(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db_host = crud.host.get_default_with_user(db, user=current_user)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host


@router.get("/{host_id}", response_model=Host)
def read_host(
    host_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_host = crud.host.get(db, host_id)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host


@router.put("/{host_id}", response_model=Host)
def update_host(
    host_id: UUID,
    host: HostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_host = crud.host.update(db, host_id, host)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host


@router.delete("/{host_id}", response_model=Host)
def delete_host(
    host_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_host = crud.host.delete(db, host_id)
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host
