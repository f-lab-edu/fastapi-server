import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select

from api.api_schema import UserSign
from database import User, engine
from main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_test_environment():
    # 테스트 환경 설정
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # teardown
    SQLModel.metadata.drop_all(engine)
    session.close()


def test_success_create_user(setup_test_environment):
    session = setup_test_environment

    # given

    # when : 유저 생성 성공
    user_sign = UserSign(user_id="admin01", password="A1234567890", nickname="admin")
    user_sign_data = user_sign.dict()
    response = client.post("/api/users/", json=user_sign_data)

    # then
    assert response.status_code == 201
    assert response.json().get("message") == "유저 생성 성공"

    # 데이터베이스에서 유저 조회
    db_user = session.exec(
        select(User).where(User.user_id == user_sign_data.get("user_id"))
    ).first()
    assert db_user is not None  # 실제로 유저가 생성되었는지 확인
    assert db_user.nickname == user_sign_data.get(
        "nickname"
    )  # 생성된 유저의 닉네임이 기대하는 값과 일치하는지 확인
