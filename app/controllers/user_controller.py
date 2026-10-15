from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# from app.models.account_model import Account
from app.models.user_model import User
# from app.schemas.user_schema import UserCreate, UserUpdate
# from app.services.security import hash_password


# def create_user(data: UserCreate, db: Session) -> User:
#     if db.query(User).filter(User.email == data.email).first():
#         raise HTTPException(status_code=409, detail="Email already registered")

#     if db.query(Account).filter(Account.iban == data.iban).first():
#         raise HTTPException(status_code=409, detail="IBAN already registered")

#     user = User(
#         name=data.name,
#         email=data.email,
#         password=hash_password(data.password),
#     )

#     try:
#         db.add(user)
#         db.flush()

#         account = Account(
#             user_id=user.id,
#             iban=data.iban,
#             balance=Decimal("0.00"),
#         )
#         db.add(account)
#         db.commit()
#         db.refresh(user)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(
#             status_code=409,
#             detail="Email or IBAN already registered",
#         )

#     return user


# def get_user_list(db: Session) -> list[User]:
#     return db.query(User).all()


def get_user(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# def update_user(user_id: int, data: UserUpdate, db: Session) -> User:
#     user = get_user(user_id, db)
#     changes = data.model_dump(exclude_unset=True)

#     iban = changes.pop("iban", None)

#     if "password" in changes:
#         changes["password"] = hash_password(changes["password"])

#     for field, value in changes.items():
#         setattr(user, field, value)

#     if iban is not None:
#         account = (
#             db.query(Account)
#             .filter(Account.user_id == user_id)
#             .first()
#         )
#         if account is None:
#             raise HTTPException(status_code=404, detail="Account not found")

#         existing_account = (
#             db.query(Account)
#             .filter(Account.iban == iban, Account.user_id != user_id)
#             .first()
#         )
#         if existing_account:
#             raise HTTPException(status_code=409, detail="IBAN already registered")

#         account.iban = iban

#     db.commit()
#     db.refresh(user)
#     return user


# def delete_user(user_id: int, db: Session) -> None:
#     user = get_user(user_id, db)
#     db.delete(user)
#     db.commit()