from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.transfer_model import Transfer
from app.schemas.transfer_schema import TransferCreate

# TODOS compañero: ajustar esta ruta cuando exista el modelo Account.
# Ej. from app.models.account_model import Account
from app.models.account_model import Account  # type: ignore


def create_new_transfer(db: Session, transfer_data: TransferCreate, current_user_id: int):
    # 1. Cuenta emisora (asume 1 cuenta por usuario)
    sender = db.query(Account).filter(Account.id == current_user_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender account not found")

    if sender.id == transfer_data.recipient_account_id:
        raise HTTPException(status_code=400, detail="You cannot transfer money to your own account")

    # 2. Saldo suficiente
    if sender.balance < transfer_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 3. Cuenta destino
    recipient = db.query(Account).filter(Account.id == transfer_data.recipient_account_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient account not found")

    # 4. Transacción segura: todo o nada
    try:
        sender.balance -= transfer_data.amount
        recipient.balance += transfer_data.amount

        new_transfer = Transfer(
            sender_account_id=sender.id,
            recipient_account_id=recipient.id,
            amount=transfer_data.amount,
            concept=transfer_data.concept,
        )
        db.add(new_transfer)
        db.commit()
        db.refresh(new_transfer)
        return new_transfer
    except Exception:
        db.rollback()
        raise


def get_user_transfer_history(db: Session, current_user_id: int):
    return (
        db.query(Transfer)
        .filter(
            or_(
                Transfer.sender_account_id == current_user_id,
                Transfer.recipient_account_id == current_user_id,
            )
        )
        .all()
    )