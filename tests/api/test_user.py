from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select

from api.api_schema import Login, UserBody, UserRole, UserSign
from api.user import add_token_to_db, is_token_in_db
from common import encode_access_token, password_hashing, settings, verify_password
from database import Comment, Post, User, engine
from main import app

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    # setup
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # teardown
    # SQLModel.metadata.drop_all(engine)
    session.close()


def test_fail404_sign_in_user():
    # when
    sign_in = Login(user_id="admin001", password="1234567890")
    response = client.post("/api/users/login", json=sign_in.dict())
    res_data = response.json()

    # then
    assert response.status_code == 404
    assert res_data["detail"] == "유저 아이디가 존재하지 않습니다."


def test_fail401_sign_in_user(setup_test_environment):
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
    sign_in = Login(user_id="admin001", password="A123456789")
    response = client.post("/api/users/login", json=sign_in.dict())
    res_data = response.json()

    # then
    assert response.status_code == 401
    assert res_data["detail"] == "아이디 혹은 비밀번호가 맞지 않습니다."


def test_success_sign_in_user(setup_test_environment):
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
    sign_in = Login(user_id="admin002", password="A1234567890")
    sign_in_data = sign_in.dict()
    response = client.post("/api/users/login", json=sign_in_data)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert is_token_in_db(res_data["access_token"]) == True

    # 데이터베이스에서 유저 조회
    db_user = session.exec(
        select(User).where(User.user_id == sign_in_data.get("user_id"))
    ).first()
    assert db_user is not None  # 실제로 유저가 있는지 확인


def test_success_logout_user():
    # given
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin001"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    # when : 로그아웃 성공
    response = client.post("/api/users/logout", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "로그아웃 성공"


def test_success_create_user(setup_test_environment):
    session = setup_test_environment

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
    assert db_user.user_id == user_sign_data.get("user_id")
    assert verify_password(user_sign_data.get("password"), db_user.password) == True
    assert db_user.nickname == user_sign_data.get(
        "nickname"
    )  # 생성된 유저의 닉네임이 기대하는 값과 일치하는지 확인


def test_success_edit_user(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin02",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin02"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    # when
    user_edit_data = UserBody(nickname="editadmin", password="1234567890A")
    response = client.put(
        "/api/users/admin02", json=user_edit_data.dict(), headers=headers
    )
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "유저 아이디 admin02 수정 성공"
    assert res_data["data"]["user_id"] == "admin02"
    assert verify_password("1234567890A", res_data["data"]["password"]) == True
    assert res_data["data"]["nickname"] == "editadmin"


def test_success_delete_user(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin03",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin03"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    # when
    response = client.delete("/api/users/admin03", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "유저 아이디 admin03 삭제 성공"


def test_success_get_user_posts(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin04",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin04"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin04", title="테스트 제목", content="테스트 내용")
    session.add(post)
    session.commit()

    # when
    response = client.get("/api/users/admin04/posts/1", headers=headers)

    # then
    assert response.status_code == 200


def test_success_get_user_comments(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin05",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin05"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin05", title="테스트 제목", content="테스트 내용")
    session.add(post)
    session.commit()
    data = Comment(author_id="admin05", post_id=2, content="댓글 내용")
    session.add(data)
    session.commit()

    # when
    response = client.get("/api/users/admin001/comments/1", headers=headers)

    # then
    assert response.status_code == 200
