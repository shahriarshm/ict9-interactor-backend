from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.schemas.discount_code import (
    DiscountCode,
    DiscountCodeCreate,
    DiscountCodeUpdate,
)
from app.api import deps
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=DiscountCode)
def create_discount_code(
    discount_code: DiscountCodeCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Check if the user owns the campaign
    campaign = crud.campaign.get(db, id=discount_code.campaign_id)
    if not campaign or campaign.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create discount code for this campaign",
        )
    return crud.discount_code.create_with_campaign(
        db=db, obj_in=discount_code, campaign_id=discount_code.campaign_id
    )


@router.get("/", response_model=List[DiscountCode])
def read_discount_codes(
    skip: int = 0,
    limit: int = 100,
    campaign_id: UUID = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if campaign_id:
        # Check if the user owns the campaign
        campaign = crud.campaign.get(db, id=campaign_id)
        if not campaign or campaign.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view discount codes for this campaign",
            )
        discount_codes = crud.discount_code.get_discount_codes_by_campaign(
            db, campaign_id=campaign_id
        )
    else:
        discount_codes = crud.discount_code.get_multi(db, skip=skip, limit=limit)
    return discount_codes


@router.get("/{discount_code_id}", response_model=DiscountCode)
def read_discount_code(
    discount_code_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    discount_code = crud.discount_code.get(db, id=discount_code_id)
    if not discount_code:
        raise HTTPException(status_code=404, detail="Discount code not found")
    # Check if the user owns the campaign associated with the discount code
    campaign = crud.campaign.get(db, id=discount_code.campaign_id)
    if not campaign or campaign.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this discount code"
        )
    return discount_code


@router.put("/{discount_code_id}", response_model=DiscountCode)
def update_discount_code(
    discount_code_id: UUID,
    discount_code: DiscountCodeUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_discount_code = crud.discount_code.get(db, id=discount_code_id)
    if not db_discount_code:
        raise HTTPException(status_code=404, detail="Discount code not found")
    # Check if the user owns the campaign associated with the discount code
    campaign = crud.campaign.get(db, id=db_discount_code.campaign_id)
    if not campaign or campaign.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this discount code"
        )
    return crud.discount_code.update(db, db_obj=db_discount_code, obj_in=discount_code)


@router.delete("/{discount_code_id}", response_model=DiscountCode)
def delete_discount_code(
    discount_code_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    discount_code = crud.discount_code.get(db, id=discount_code_id)
    if not discount_code:
        raise HTTPException(status_code=404, detail="Discount code not found")
    # Check if the user owns the campaign associated with the discount code
    campaign = crud.campaign.get(db, id=discount_code.campaign_id)
    if not campaign or campaign.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this discount code"
        )
    return crud.discount_code.remove(db, id=discount_code_id)
