from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import account_controller
from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user_model import User
from app.schemas.account_schema import AccountResponse

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/me", response_model=AccountResponse, summary="Fetch my account")
def get_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return account_controller.get_account_for_user(db, current_user.id)