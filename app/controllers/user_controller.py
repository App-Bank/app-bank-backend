from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
# TODO: check `hash_password` implementation
# from app.security import hash_password


def get_user_list(db: Session) -> list[User]:
    return db.query(User).all()


def get_user(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(data: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        # password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(user_id: int, data: UserUpdate, db: Session) -> User:
    user = get_user(user_id, db)
    changes = data.model_dump(exclude_unset=True)

    # if "password" in changes:
    #     changes["password"] = hash_password(changes["password"])

    for field, value in changes.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int, db: Session) -> None:
    user = get_user(user_id, db)
    db.delete(user)
    db.commit()