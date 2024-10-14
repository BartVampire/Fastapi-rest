import jwt
from app.core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str =settings.auth.private_key_path.read_text(),
        algorithm: str =settings.auth.algorithm
): # Функция кодирования токена JWT с использованием RS256 алгоритма
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth.public_key_path.read_text(),
        algorithms: str = settings.auth.algorithm
): # Функция декодирования токена JWT с использованием RS256 алгоритма
    decoded = jwt.decode(token, public_key, algorithms=[algorithms])
    return decoded