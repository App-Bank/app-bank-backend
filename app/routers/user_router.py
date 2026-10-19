from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/me", response_model=UserResponse, summary="Fetch my profile")
def get_my_user(
    current_user: User = Depends(get_current_user),
):
    return current_user