import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from api.api_schema import Login, UserRole
from common import password_hashing
from database import User
from main import app

client = TestClient(app)


@pytest.fixture
def setup_test_environment():
    # setup
    sqlite_file_name = ":memory:"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin001",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()

    yield session

    # teardown
    session.close()


def test_fail404_login_user(setup_test_environment):
    session = setup_test_environment
    # given

    # when : 회원정보에 없는 로그인 시도
    login = Login(user_id="admin001", password="1234567890")
    login_data = login.dict()
    response = client.post("/api/users/login", json=login_data)

    # then
    assert response.status_code == 404
    assert response.json().get("detail") == "유저 아이디가 존재하지 않습니다."


def test_fail401_login_user(setup_test_environment):
    session = setup_test_environment

    # given

    # when : 틀린 비밀번호로 로그인 시도
    login = Login(user_id="admin", password="A123456789")
    login_data = login.dict()
    response = client.post("/api/users/login", json=login_data)

    # then
    assert response.status_code == 401
    assert response.json().get("detail") == "아이디 혹은 비밀번호가 맞지 않습니다."


def test_success_login_user(setup_test_environment):
    session = setup_test_environment

    # given

    # when : 로그인 성공
    login = Login(user_id="admin", password="A1234567890")
    login_data = login.dict()
    response = client.post("/api/users/login", json=login_data)

    # then
    assert response.status_code == 200
