from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.core.database import get_db
from app.schemas.user_schema import UserResponse 

router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Fetch a user"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user(user_id, db)