from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select

from api.api_schema import RequestBody, UserRole
from api.user import add_token_to_db
from common import encode_access_token, password_hashing, settings
from database import Comment, Post, User, engine
from main import app

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    # setup
    SQLModel.metadata.create_all(engine)

    yield

    # teardown
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session():
    with Session(engine) as session:
        yield session
        session.rollback()


def test_success_create_post(db_session):
    session = db_session

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin0001",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin0001"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    # when
    post_request_body = RequestBody(
        author="admin0001", title="게시물 제목", content="게시물 내용"
    )
    response = client.post(
        "/api/posts/", json=post_request_body.dict(), headers=headers
    )
    res_data = response.json()

    # then
    assert response.status_code == 201
    assert res_data["message"] == "게시글 생성 성공"

    db_user = session.exec(select(User).where(User.user_id == "admin0001")).first()
    db_post = session.exec(select(Post).where(Post.post_id == 1)).first()
    assert db_user is not None  # 실제로 유저가 있는지 확인
    assert db_user.user_id == "admin0001"
    assert db_post.post_id == 1
    assert db_post.title == "게시물 제목"
    assert db_post.content == "게시물 내용"


def test_success_get_post_list():
    # when
    response = client.get("/api/posts/?page=1")
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "게시글 목록 조회 성공"


def test_success_get_post(db_session):
    session = db_session

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin0023",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin0023"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin0023", title="게시물 제목", content="게시물 내용")
    session.add(post)
    session.commit()

    # when
    response = client.get("/api/posts/1", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "게시글 조회 성공"


def test_success_edit_post(db_session):
    session = db_session

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin0044",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin0044"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin0044", title="게시물 제목", content="게시물 내용")
    session.add(post)
    session.commit()

    # when
    editor_request_body = RequestBody(
        author="admin0044", title="게시물 제목 변경", content="변경된 게시물 내용"
    )
    response = client.put(
        "/api/posts/6", json=editor_request_body.dict(), headers=headers
    )
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "게시글 번호 6 수정 성공"


def test_success_delete_post(db_session):
    session = db_session

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin0055",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin0055"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin0055", title="게시물 제목", content="게시물 내용")
    session.add(post)
    session.commit()

    # when
    response = client.delete("/api/posts/7", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "게시글 번호 7 삭제 성공"


def test_success_get_post_comments(db_session):
    session = db_session

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin0066",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin0066"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}
    post = Post(author="admin0066", title="게시물 제목", content="게시물 내용")
    session.add(post)
    session.commit()
    comment = Comment(author_id="admin0066", post_id=1, content="댓글 내용")
    session.add(comment)
    session.commit()

    # when
    response = client.get("/api/posts/1/comments/?page=1")
    res_data = response.json()

    # then
    assert response.status_code == 200
    assert res_data["message"] == "게시글 별로 작성된 댓글 목록 조회 성공"
