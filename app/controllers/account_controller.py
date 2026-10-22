from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.account_model import Account


def get_account_for_user(db: Session, user_id: int) -> Account:
    account = (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .first()
    )
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account