from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud
from app.schemas.campaign import (
    Campaign,
    CampaignCreate,
    CampaignUpdate,
    CampaignStatus,
)
from app.api import deps
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=Campaign)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Check if the user owns the host
    host = crud.host.get(db, id=campaign.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to create campaign for this host"
        )
    return crud.campaign.create_with_user_and_host(
        db=db, obj_in=campaign, user_id=current_user.id, host_id=campaign.host_id
    )


@router.get("/", response_model=List[Campaign])
def read_campaigns(
    skip: int = 0,
    limit: int = 100,
    host_id: Optional[UUID] = None,
    status: Optional[CampaignStatus] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    filters = []
    if host_id:
        # Check if the user owns the host
        host = crud.host.get(db, id=host_id)
        if not host or host.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to view campaigns for this host"
            )
        filters.append(("host_id", host_id))
    if status:
        filters.append(("status", status))

    campaigns = crud.campaign.get_multi_with_filters(
        db, skip=skip, limit=limit, filters=filters
    )
    return campaigns


@router.get("/{campaign_id}", response_model=Campaign)
def read_campaign(
    campaign_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    campaign = crud.campaign.get(db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    # Check if the user owns the host associated with the campaign
    host = crud.host.get(db, id=campaign.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this campaign"
        )
    return campaign


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: UUID,
    campaign: CampaignUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    db_campaign = crud.campaign.get(db, id=campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    # Check if the user owns the host associated with the campaign
    host = crud.host.get(db, id=db_campaign.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this campaign"
        )
    return crud.campaign.update(db, db_obj=db_campaign, obj_in=campaign)


@router.delete("/{campaign_id}", response_model=Campaign)
def delete_campaign(
    campaign_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    campaign = crud.campaign.get(db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    # Check if the user owns the host associated with the campaign
    host = crud.host.get(db, id=campaign.host_id)
    if not host or host.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this campaign"
        )
    return crud.campaign.remove(db, id=campaign_id)
