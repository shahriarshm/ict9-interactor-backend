from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.schemas.user import Token, UserCreate, UserLogin, UserUpdate, User
from app.api import deps
from app.config import settings
from app.security import create_access_token
from app.schemas.host import HostCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.user.create(db=db, obj_in=user)

    # Create default host for the new user
    default_host = HostCreate(name=f"Default Host")
    crud.host.create_with_user(db=db, obj_in=default_host, user=new_user)

    return new_user


@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.update(db, db_obj=db_user, obj_in=user)


@router.delete("/{user_id}", response_model=User)
def delete_user(
    user_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.remove(db, id=user_id)


@router.post("/token", response_model=Token)
async def login_for_access_token(data: UserLogin, db: Session = Depends(deps.get_db)):
    user = crud.user.authenticate(db, email=data.email, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
