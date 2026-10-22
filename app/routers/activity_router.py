from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user_model import User
from app.schemas.activity_schema import ActivityResponse
from app.controllers.activity_controller import get_user_activities

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.get("", response_model=List[ActivityResponse])
def list_my_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    return get_user_activities(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )