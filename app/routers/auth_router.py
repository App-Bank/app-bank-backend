from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.auth_controller import login
from app.core.database import get_db
from app.schemas.user_schema import UserLogin, TokenResponse 

router = APIRouter(prefix="/auth/login", tags=["Authentication"])

@router.post(
    "",
    response_model=TokenResponse,
    summary="Login a user"
)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    return login(user, db)




