import os

import pytest
from dotenv import load_dotenv

load_dotenv()


def pytest_configure():
    os.environ["TEST_ENV"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///tests.db"


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    # 여기에 테스트 세션 시작 전 실행할 코드를 작성 (필요한 경우)
    # 예: 테스트용 데이터베이스 초기화, 테스트용 파일 생성 등
    pytest_configure()

    yield

    # 테스트 세션이 끝난 후 실행할 정리 코드
    # 예: 테스트 파일 삭제
    os.remove("test.db")
