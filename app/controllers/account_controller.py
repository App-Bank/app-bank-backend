from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.account_model import Account


# TODO: adapt code to match auth feature (currently logged user GETs his linked account data).
def get_account(account_id: int, db: Session) -> Account:
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account