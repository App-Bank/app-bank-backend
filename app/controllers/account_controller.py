from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.account_model import Account


def get_account(account_id: int, db: Session) -> Account:
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account