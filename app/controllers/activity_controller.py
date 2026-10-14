from app.models.account_model import Account
from app.models.timezone_model import Timezone
from app.models.transfer_model import Transfer
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.activity_model import Activity
from app.models.activity_type_model import ActivityType
from app.schemas.activity_schema import ActivityCreate


def get_activity(db:Session, skip:int = 0, limit: int = 50) -> list[Activity]:
    try:
        return db.query(Activity).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la consulta de movimientos {str(error)}"  # noqa: RUF010
        )   

def exist(db:Session, model_name:Transfer|Account|ActivityType|Timezone, id:int)->None:
    existing = db.query(model_name).filter(model_name.id == id).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name.__name__} with ID {id} not found"
        )


def create_activity(db:Session, activity_data: ActivityCreate) -> Activity:
    new_activity = Activity(
        amount=activity_data.amount,
        succeeded_in=activity_data.succeeded_in,
        transfer_id=activity_data.transfer_id,
        account_id=activity_data.account_id,
        activity_type_id=activity_data.activity_type_id,
        timezone_id=activity_data.timezone_id
    )
    exist(db, Transfer, activity_data.transfer_id)
    exist(db, Account, activity_data.account_id)
    exist(db, ActivityType, activity_data.activity_type_id)
    exist(db, Timezone, activity_data.timezone_id)

    try:
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity
    
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la creacion de movimiento en la base de datos {str(error)}"  # noqa: RUF010
        )
