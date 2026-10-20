from sqlalchemy.orm import Session

from app.models.activity_model import Activity
from app.models.account_model import Account


def get_user_activities(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
):
    account_exist = db.query(Account).filter(Account.user_id == user_id).first()
    if not account_exist:
        return []
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
        .join(Account, Activity.account_id == Account.id)
        .filter(Account.user_id == user_id)
        .order_by(Activity.succeeded_in.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )