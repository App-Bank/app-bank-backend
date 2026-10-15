from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.account_model import Account
from app.models.timezone_model import Timezone
from app.models.user_model import User


def run_seed(db: Session):
    # 1. Zonas horarias (idempotente por name)
    timezones = [
        {"name": "Europe/Madrid", "offset": "+01:00"},
        {"name": "Atlantic/Canary", "offset": "+00:00"},
    ]
    for tz in timezones:
        exists = db.query(Timezone).filter(Timezone.name == tz["name"]).first()
        if not exists:
            db.add(Timezone(name=tz["name"], offset=tz["offset"]))
    db.commit()

    # 2. Usuarios de prueba (idempotente por email)
    users = [
        {"name": "User Uno", "email": "user1@banco.com", "password": "test1234"},
        {"name": "User Dos", "email": "user2@banco.com", "password": "test1234"},
    ]
    for u in users:
        exists = db.query(User).filter(User.email == u["email"]).first()
        if not exists:
            db.add(User(name=u["name"], email=u["email"], password=u["password"]))
    db.commit()

    # 3. Cuentas (integridad referencial: resuelve user_id real)
    user1 = db.query(User).filter(User.email == "user1@banco.com").first()
    user2 = db.query(User).filter(User.email == "user2@banco.com").first()

    accounts = [
        {"user": user1, "iban": "ES9121000418450200051332", "balance": Decimal("1000.00")},
        {"user": user2, "iban": "ES9121000418450200051333", "balance": Decimal("500.00")},
    ]
    for acc in accounts:
        if acc["user"] is None:
            continue
        exists = db.query(Account).filter(Account.iban == acc["iban"]).first()
        if not exists:
            db.add(
                Account(
                    user_id=acc["user"].id,
                    iban=acc["iban"],
                    balance=acc["balance"],
                )
            )
    db.commit()
