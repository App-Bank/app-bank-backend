from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.account_model import Account
from app.models.user_model import User
from app.schemas.account_schema import AccountCreate


def create_account(data: AccountCreate, db: Session) -> Account:
    user = db.get(User, data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(Account).filter(Account.iban == data.iban).first()
    if existing:
        raise HTTPException(status_code=409, detail="IBAN already registered")

    account = Account(
        user_id=data.user_id,
        iban=data.iban,
        balance=data.balance
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def list_accounts(db: Session) -> list[Account]:
    return db.query(Account).all()


def get_account(account_id: int, db: Session) -> Account:
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account