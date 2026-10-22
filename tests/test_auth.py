import os

os.environ.setdefault("AUTH_SECRET_KEY", "test_secret_key_1234567890")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_banco.db")

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.models.user_model import User
from app.routers import auth_router
from app.services.security import hash_password

app = FastAPI(title="Bank App API - Auth Tests")
app.include_router(auth_router.router)


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
    db.add_all([
        User(
            id=1,
            name="User Uno",
            email="user1@banco.com",
            password_hash=hash_password("test1234"),
        ),
        User(
            id=2,
            name="User Dos",
            email="user2@banco.com",
            password_hash=hash_password("test1234"),
        ),
    ])
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_login_success(client):
    response = client.post(
        "/auth/login",
        json={"email": "user1@banco.com", "password": "test1234"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]
