from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select

from api.api_schema import Login, UserRole, UserSign
from api.user import add_token_to_db, is_token_in_db
from common import encode_access_token, password_hashing, settings
from database import AuthToken, User, engine
from main import app

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    # setup
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # teardown
    SQLModel.metadata.drop_all(engine)
    session.close()


def test_fail404_login_user():
    # when
    login = Login(user_id="admin001", password="1234567890")
    response = client.post("/api/users/login", json=login.dict())
    res_data = response.json()

    # then
    assert response.status_code == 404
    assert res_data["detail"] == "유저 아이디가 존재하지 않습니다."


def test_fail401_login_user(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin001",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()

    # when : 틀린 비밀번호로 로그인 시도
    login = Login(user_id="admin001", password="A123456789")
    response = client.post("/api/users/login", json=login.dict())
    res_data = response.json()

    # then
    assert response.status_code == 401
    assert res_data["detail"] == "아이디 혹은 비밀번호가 맞지 않습니다."


def test_success_login_user(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin002",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()

    # when : 로그인 성공
    login = Login(user_id="admin002", password="A1234567890")
    login_data = login.dict()
    response = client.post("/api/users/login", json=login_data)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert is_token_in_db(res_data["access_token"]) == True

    # 데이터베이스에서 유저 조회
    db_user = session.exec(
        select(User).where(User.user_id == login_data.get("user_id"))
    ).first()
    assert db_user is not None  # 실제로 유저가 있는지 확인


def test_success_logout_user():
    # given
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin001"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)

    headers = {"Authorization": f"Bearer {access_token}"}

    # when : 로그아웃 성공
    response = client.post("/api/users/logout", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert is_token_in_db(res_data["access_token"]) == False


def test_success_create_user(setup_test_environment):
    session = setup_test_environment

    # given

    # when : 유저 생성 성공
    user_sign = UserSign(user_id="admin01", password="A1234567890", nickname="admin")
    user_sign_data = user_sign.dict()
    response = client.post("/api/users/", json=user_sign_data)
    res_data = response.json()

    # then
    assert response.status_code == 201
    assert res_data["message"] == "유저 생성 성공"

    # 데이터베이스에서 유저 조회
    db_user = session.exec(
        select(User).where(User.user_id == user_sign_data.get("user_id"))
    ).first()
    assert db_user is not None  # 실제로 유저가 생성되었는지 확인
    assert db_user.nickname == user_sign_data.get(
        "nickname"
    )  # 생성된 유저의 닉네임이 기대하는 값과 일치하는지 확인
