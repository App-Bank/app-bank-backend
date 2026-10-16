from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import account_controller
from app.core.database import get_db
from app.schemas.account_schema import AccountResponse

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="Fetch all accounts",
)
def list_accounts(db: Session = Depends(get_db)):
    return account_controller.list_accounts(db)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Fetch an account",
)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return account_controller.get_account(account_id, db)