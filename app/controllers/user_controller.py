from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import User


def get_user(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user