from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user"
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(data, db)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Fetch all users"
)
def get_user_list(db: Session = Depends(get_db)):
    return user_controller.get_user_list(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Fetch a user"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user(user_id, db)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Edit a user"
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    return user_controller.update_user(user_id, data, db)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user"
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_controller.delete_user(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)