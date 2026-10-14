from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import account_controller
from app.core.database import get_db
from app.schemas.account_schema import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    "/",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an account"
)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return account_controller.create_account(data, db)


@router.get(
    "/",
    response_model=list[AccountResponse],
    summary="Fetch all accounts"        
)
def list_accounts(db: Session = Depends(get_db)):
    return account_controller.list_accounts(db)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Fetch an account"
)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return account_controller.get_account(account_id, db)