from sqlalchemy.orm import Session

from app.models.timezone_model import Timezone


def get_all_timezones(db: Session):
    return db.query(Timezone).all()