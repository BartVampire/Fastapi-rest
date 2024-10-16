from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from app.api.auth_v1.auth_crud import users_db
from app.api.auth_v1.auth_helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.auth import utils_jwt
from app.core.schemas import user_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> user_schemas.UserSchema:
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный токен.",
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Тип токена неверный."
    )


def get_user_by_token_sub(payload: dict) -> user_schemas.UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Вы не зарегистрированы.",
    )


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> user_schemas.UserSchema:
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload=payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> user_schemas.UserSchema:
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload=payload)


def get_current_active_auth_user(
    user: user_schemas.UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Не подтвержденный пользователь.",
    )


def validate_auth_user(username: str = Form(), password: str = Form()):
    un_authed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неправильный логин или пароль.",
    )
    if not (user := users_db.get(username)):
        raise un_authed_exception
    if not utils_jwt.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise un_authed_exception
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не подтвержденный пользователь.",
        )
    return user
