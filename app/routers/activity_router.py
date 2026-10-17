from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers.activity_controller import create_activity
from app.core.database import get_db
from app.schemas.activity_schema import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activity", tags=["Activity"])


# NOTE: `GET Activity` is never used but `GET Transfer` is instead
# @router.get(
#     "",
#     response_model=list[ActivityResponse],
#     summary="Read a activity",
#     description="Seen all activities"
# )
# def read_activities(
#     skip:int =Query(0,ge=0,description="Starting row number to display"),
#     limit:int =Query(50,ge=1, le=50,description="Number of row limits"),
#     db: Session = Depends(get_db)
# ):
#     return get_activity(db=db, skip=skip, limit=limit)

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