from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers.activity_controller import create_activity
from app.core.database import get_db
from app.schemas.activity_schema import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.post(
    "",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new activity"
)

def create_new_activity(
    activity_data:ActivityCreate,
    db:Session = Depends(get_db)
):
    return create_activity(db=db, activity_data=activity_data)