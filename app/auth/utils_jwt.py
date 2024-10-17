import os
import bcrypt
from datetime import datetime, UTC, timedelta
from dotenv import load_dotenv

load_dotenv()

import jwt
from app.core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expires_minutes,
    expire_timedelta: timedelta | None = None,
):  # Функция кодирования токена JWT с использованием RS256 алгоритма
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth.public_key_path.read_text(),
    algorithms: str = settings.auth.algorithm,
):  # Функция декодирования токена JWT с использованием RS256 алгоритма
    decoded = jwt.decode(token, public_key, algorithms=[algorithms])
    return decoded


# Глобальная переменная для pepper (должна храниться в безопасном месте, например, в переменных окружения)
PEPPER = os.getenv("FASTAPI__FIRST__PEPPER").encode()
JOKE_PEPPER = os.getenv("FASTAPI__SECOND__PEPPER").encode()


def hash_password(password: str) -> bytes:  # Функция хеширования пароля
    salt = bcrypt.gensalt()
    peppered_password: bytes = password.encode() + PEPPER
    pwd_bytes_first: bytes = bcrypt.hashpw(peppered_password, salt)
    pwd_bytes_last: bytes = JOKE_PEPPER + pwd_bytes_first
    return pwd_bytes_last


def validate_password(
    password: str, hashed_password: bytes
) -> bool:  # Функция валидации пароля по хешу
    password = password.encode() + PEPPER
    hashed_password = hashed_password[5:]
    return bcrypt.checkpw(password=password, hashed_password=hashed_password)
