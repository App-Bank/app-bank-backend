from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers.activity_type_controller import (
    create_activity_type,
    get_activity_types,
)
from app.core.database import get_db
from app.schemas.activity_type_schema import ActivityTypeCreate, ActivityTypeResponse

router = APIRouter(
    prefix="/activity_type",
    tags=["Activity Type"]
)

@router.get(
    "",
    response_model=list[ActivityTypeResponse],
    summary="Read a activity type",
    description="Seen all activity types"
)
def read_activities(
    skip:int =Query(0,ge=0,description="Starting row number to display"),
    limit:int =Query(50,ge=1, le=50,description="Number of row limits"),
    db: Session = Depends(get_db)
):
    return get_activity_types(db=db, skip=skip, limit=limit)

@router.post(
    "",
    response_model=ActivityTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new activity type",
    description="Add a new activity type",
)

def create_new_activity_type(
    activity_type_data:ActivityTypeCreate,
    db:Session =Depends(get_db)
):
    return create_activity_type(db=db, activity_type_data=activity_type_data)