import os

from dotenv import load_dotenv

load_dotenv()


def pytest_configure():
    os.environ["TEST_ENV"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///tests.db"
