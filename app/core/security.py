from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_PRIVATE_KEY_PATH,
    JWT_PUBLIC_KEY_PATH,
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _read_private_key() -> str:
    with open(JWT_PRIVATE_KEY_PATH, "r", encoding="utf-8") as file:
        return file.read()


def _read_public_key() -> str:
    with open(JWT_PUBLIC_KEY_PATH, "r", encoding="utf-8") as file:
        return file.read()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    private_key = _read_private_key()
    return jwt.encode(to_encode, private_key, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    public_key = _read_public_key()
    return jwt.decode(token, public_key, algorithms=[JWT_ALGORITHM])
