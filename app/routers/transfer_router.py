from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import transfer_controller
from app.core.database import get_db
from app.schemas.transfer_schema import TransferCreate, TransferResponse

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.post("/", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(transfer_data: TransferCreate, db: Session = Depends(get_db)):
    # TODO auth: aquí se conectará el sistema de autenticación (get_current_user)
    current_user_id = 1
    return transfer_controller.create_new_transfer(db, transfer_data, current_user_id)


@router.get("/history", response_model=List[TransferResponse])
def transfer_history(db: Session = Depends(get_db)):
    # TODO auth: mismo current_user simulado hasta tener login real
    current_user_id = 1
    return transfer_controller.get_user_transfer_history(db, current_user_id)