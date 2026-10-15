from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.transfer_model import Transfer
from app.schemas.transfer_schema import TransferCreate

# TODOS compañero: ajustar esta ruta cuando exista el modelo Account.
# Ej. from app.models.account_model import Account
from app.models.account_model import Account  # type: ignore


def create_new_transfer(db: Session, transfer_data: TransferCreate, current_user_id: int):
    # 1. Cuenta emisora por usuario (campo real del compañero)
    sender_account = db.query(Account).filter(Account.user_id == current_user_id).first()
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")

    if sender_account.id == transfer_data.recipient_account_id:
        raise HTTPException(status_code=400, detail="You cannot transfer money to your own account")

    # 2. Saldo suficiente
    if sender_account.balance < transfer_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 3. Cuenta destino
    recipient = db.query(Account).filter(Account.id == transfer_data.recipient_account_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient account not found")

    # 4. Transacción segura: todo o nada
    try:
        sender_account.balance -= transfer_data.amount
        recipient.balance += transfer_data.amount

        new_transfer = Transfer(
            sender_account_id=sender_account.id,
            recipient_account_id=recipient.id,
            amount=transfer_data.amount,
            concept=transfer_data.concept,
            timezone_id=transfer_data.timezone_id,
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