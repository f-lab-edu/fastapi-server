from datetime import datetime, timedelta, timezone
from typing import Dict, Union

import yaml
from fastapi.security import APIKeyHeader
from jose import jwt
from passlib.context import CryptContext

from config import Settings

api_key_header = APIKeyHeader(name="Authorization")

password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")

with open("config.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)

settings = Settings(
    secret_key=yaml_data.get("secret_key"),
    algorithm=yaml_data.get("algorithm"),
    access_token_expire_days=yaml_data.get("access_token_expire_days"),
)


def encode_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_password(plain_password, hashed_password) -> bool:
    return password_hashing.verify(plain_password, hashed_password)


def decode_access_token(token) -> Dict[str, Union[str, int]]:
    decoded_jwt = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    return decoded_jwt
