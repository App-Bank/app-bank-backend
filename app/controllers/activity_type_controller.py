from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.activity_type_model import ActivityType
from app.schemas.activity_type_schema import ActivityTypeCreate


def get_activity_types(db:Session, skip:int = 0, limit: int = 50) -> list[ActivityType]:
    try:
        return db.query(ActivityType).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when querying activity types"
        )   



def create_activity_type(db:Session, activity_type_data: ActivityTypeCreate) -> ActivityType:
    new_activity_type = ActivityType(
        name=activity_type_data.name
    )

    try:
        db.add(new_activity_type)
        db.commit()
        db.refresh(new_activity_type)
        return new_activity_type
    
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when creating activity type in the database"
        )