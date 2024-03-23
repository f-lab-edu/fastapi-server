import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from api.api_schema import UserSign
from database import engine
from main import app

client = TestClient(app)


@pytest.fixture()
def setup_test_environment():
    # 테스트 환경 설정
    # os.environ["TEST_ENV"] = "True"
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # teardown
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
    assert response.json().get("detail") == "유저 생성 성공"
