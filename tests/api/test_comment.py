from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from api.api_schema import CommentBody, CommentConent, UserRole
from api.user import add_token_to_db
from common import encode_access_token, password_hashing, settings
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
    session.close()


@pytest.fixture(scope="session", autouse=True)
def teardown_test_environment():
    SQLModel.metadata.drop_all(engine)


def test_success_create_comment(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin011",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin011"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    post = Post(author="admin011", title="게시물 제목 작성", content="게시물 내용")
    session.add(post)
    session.commit()

    # when
    comment_body = CommentBody(author_id="admin011", post_id=1, content="댓글 생성")
    response = client.post("/api/comments/", json=comment_body.dict())
    res_data = response.json()

    # then
    assert response.status_code == 201


def test_success_edit_comment(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin022",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin022"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    post = Post(author="admin022", title="게시물 제목 작성", content="게시물 내용")
    session.add(post)
    session.commit()

    comment = Comment(author_id="admin022", post_id=1, content="댓글 내용")
    session.add(comment)
    session.commit()

    # when
    comment_content = CommentConent(content="댓글 내용 수정")
    response = client.put(
        "/api/comments/1", json=comment_content.dict(), headers=headers
    )
    res_data = response.json()

    # then
    assert response.status_code == 200


def test_success_delete_comment(setup_test_environment):
    session = setup_test_environment

    # given
    hashed_password = password_hashing.hash("A1234567890")
    user = User(
        user_id="admin033",
        password=hashed_password,
        nickname="admin",
        role=UserRole.admin,
    )
    session.add(user)
    session.commit()
    access_token_expires = timedelta(days=settings.access_token_expire_days)
    access_token = encode_access_token(
        data={"user_id": "admin033"}, expires_delta=access_token_expires
    )
    add_token_to_db(access_token)
    headers = {"Authorization": f"{access_token}"}

    post = Post(author="admin033", title="게시물 제목 작성", content="게시물 내용")
    session.add(post)
    session.commit()

    comment = Comment(author_id="admin033", post_id=1, content="댓글 내용")
    session.add(comment)
    session.commit()

    # when : admin02 유저가 댓글 삭제 시도
    response = client.delete("/api/comments/1", headers=headers)
    res_data = response.json()

    # then
    assert response.status_code == 200
