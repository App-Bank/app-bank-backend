import os

os.environ.setdefault("AUTH_SECRET_KEY", "test_secret_key_1234567890")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_banco.db")

from decimal import Decimal

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.auth import get_current_user
from app.core.database import Base, get_db
from app.models.account_model import Account
from app.models.activity_type_model import ActivityType
from app.models.timezone_model import Timezone
from app.models.user_model import User
from app.routers import transfer_router

app = FastAPI(title="Bank App API - Transfer Tests")
app.include_router(transfer_router.router)


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = session_factory()

    sender = User(id=1, name="Sender", email="sender@test.com", password_hash="x")
    recipient = User(id=2, name="Recipient", email="recipient@test.com", password_hash="x")
    db.add_all([sender, recipient])
    db.flush()

    db.add_all([
        Timezone(id=1, name="Europe/Madrid", offset="+01:00"),
        ActivityType(id=1, name="debit"),
        ActivityType(id=2, name="credit"),
    ])
    db.add_all([
        Account(id=1, user_id=1, iban="ES0000000000000000000001", balance=Decimal("100.00")),
        Account(id=2, user_id=2, iban="ES0000000000000000000002", balance=Decimal("50.00")),
    ])
    db.commit()

    def override_get_db():
        yield db

    def override_get_current_user():
        return sender

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield TestClient(app)

    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_transfer_success(client):
    payload = {
        "recipient_account_id": 2,
        "amount": "10.00",
        "concept": "Alquiler",
        "timezone_id": 1,
    }
    response = client.post("/transfers/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert set(body.keys()) == {
        "id",
        "sender_account_id",
        "recipient_account_id",
        "amount",
        "concept",
        "timezone_id",
        "created_at",
    }
    assert body["sender_account_id"] == 1
    assert body["recipient_account_id"] == 2
    assert body["timezone_id"] == 1
    assert body["concept"] == "Alquiler"
    assert body["amount"] == "10.00"


def test_transfer_insufficient_balance(client):
    payload = {
        "recipient_account_id": 2,
        "amount": "500.00",
        "concept": "Demasiado",
        "timezone_id": 1,
    }
    response = client.post("/transfers/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_transfer_to_own_account(client):
    payload = {
        "recipient_account_id": 1,
        "amount": "10.00",
        "concept": "Auto",
        "timezone_id": 1,
    }
    response = client.post("/transfers/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot transfer money to your own account"
