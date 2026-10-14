from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.activity_type_model import ActivityType
from app.schema.activity_type_schema import ActivityTypeCreate


def get_activity_types(db:Session, skip:int = 0, limit: int = 50) -> list[ActivityType]:
    try:
        return db.query(ActivityType).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la consulta del tipo de movimiento {str(error)}"  # noqa: RUF010
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
    
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la creacion del tipo de movimiento en la base de datos {str(error)}"  # noqa: RUF010
        )
