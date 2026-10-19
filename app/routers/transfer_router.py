from typing import List

from fastapi import APIRouter, Depends, status
from app.core.auth import get_current_user
from app.models.user_model import User
from sqlalchemy.orm import Session

from app.controllers import transfer_controller
from app.core.database import get_db
from app.schemas.transfer_schema import TransferCreate, TransferResponse

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.post("/")
def create_transfer(
    transfer_data: TransferCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
        return transfer_controller.create_new_transfer(
        db, transfer_data, user.id
    )


@router.get("/history", response_model=List[TransferResponse])
def transfer_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return transfer_controller.get_user_transfer_history(db, current_user.id)