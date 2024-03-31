import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from database import engine
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
