from sqlalchemy.orm import Session
from sqlalchemy import case

from app.models.activity_model import Activity
from app.models.account_model import Account
from app.models.transfer_model import Transfer


def get_user_activities(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
):
    account_exist = db.query(Account).filter(Account.user_id == user_id).first()
    if not account_exist:
        return []
    ID_DEBIT = 1
    return (
        db.query(
            Activity.id,
            Activity.amount,
            Activity.succeeded_in,
            Activity.transfer_id,
            Activity.account_id,
            Activity.activity_type_id,
            Activity.timezone_id,
            Account.iban.label("account_iban")
            
        )
        .join(Transfer, Activity.transfer_id == Transfer.id)
        .join(
            Account,
            case(
                (Activity.activity_type_id == ID_DEBIT, Transfer.recipient_account_id == Account.id),
                else_=Transfer.sender_account_id == Account.id
            )
        )
        .filter(Activity.account_id == account_exist.id)
        .order_by(Activity.succeeded_in.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )