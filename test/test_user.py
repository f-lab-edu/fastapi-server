import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.api_schema import Login, UserRole
from common import password_hashing
from database import User, engine
from main import app

client = TestClient(app)

session = Session(engine)


@pytest.fixture
def test_create_db_user():
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin", password=hashed_password, nickname="admin", role=UserRole.admin
    )
    session.add(user)
    session.commit()


def test_login_user():
    login_data = dict(Login(user_id="admin", password="A1234567890"))
    response = client.post("/api/users/login", json=login_data)
    assert response.status_code == 200
