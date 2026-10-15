from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.account_model import Account
from app.models.activity_model import Activity
from app.models.activity_type_model import ActivityType
from app.models.transfer_model import Transfer
from app.schemas.transfer_schema import TransferCreate


def create_new_transfer(
    db: Session,
    transfer_data: TransferCreate,
    current_user_id: int,
):
    sender_account = (
        db.query(Account)
        .filter(Account.user_id == current_user_id)
        .first()
    )
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")

    if sender_account.id == transfer_data.recipient_account_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot transfer money to your own account",
        )

    recipient = (
        db.query(Account)
        .filter(Account.id == transfer_data.recipient_account_id)
        .first()
    )
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient account not found")

    if transfer_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if sender_account.balance < transfer_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Look up the IDs by their names rather than assuming fixed ID values.
    activity_types = {
        activity_type.name: activity_type.id
        for activity_type in db.query(ActivityType)
        .filter(ActivityType.name.in_(["debit", "credit"]))
        .all()
    }
    if "debit" not in activity_types or "credit" not in activity_types:
        raise HTTPException(status_code=500, detail="Required activity types are missing")

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
        db.flush()  # Assigns new_transfer.id without committing the transaction.

        timestamp = datetime.now(timezone.utc)

        db.add_all([
            Activity(
                transfer_id=new_transfer.id,
                account_id=sender_account.id,
                activity_type_id=activity_types["debit"],
                amount=transfer_data.amount,
                succeeded_in=timestamp,
                timezone_id=transfer_data.timezone_id,
            ),
            Activity(
                transfer_id=new_transfer.id,
                account_id=recipient.id,
                activity_type_id=activity_types["credit"],
                amount=transfer_data.amount,
                succeeded_in=timestamp,
                timezone_id=transfer_data.timezone_id,
            ),
        ])

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