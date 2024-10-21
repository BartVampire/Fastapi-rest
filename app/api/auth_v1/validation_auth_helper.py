from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.api.auth_v1.auth_token_helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.api.auth_v1.token_crud import is_token_blacklisted
from app.auth import utils_jwt
from app.core.models import db_helper, user_model
from app.core.schemas import user_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


async def get_current_token_payload(
    token: str | bytes = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> user_schemas.User:
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный токен.",
        )
    return payload


async def get_current_token_payload_for_refresh(
    request: Request, db: AsyncSession = Depends(db_helper.session_getter)
) -> user_schemas.User:
    try:
        token = request.cookies.get("refresh_token")
        if not token or is_token_blacklisted(db=db, refresh_token=token) is True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный токен.",
            )
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный токен.",
        )
    return payload


def validate_token_type(payload: dict, token_type: str | bytes) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Тип токена неверный."
    )


async def get_user_by_token_sub(
    payload: dict, db: AsyncSession = Depends(db_helper.session_getter)
) -> user_schemas.User:
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не зарегистрированы.",
        )
    # Запрос к базе данных для поиска пользователя по имени
    result = await db.execute(
        select(user_model.User).where(user_model.User.username == username)
    )
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден.",
        )
    return user


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> user_schemas.User:
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    return await get_user_by_token_sub(payload=payload, db=db)


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload_for_refresh),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> user_schemas.User:
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    return await get_user_by_token_sub(payload=payload, db=db)


async def get_current_active_auth_user(
    user: user_schemas.User = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Не подтвержденный пользователь.",
    )


async def get_superuser_auth(
    user: user_schemas.User = Depends(get_current_auth_user),
):
    if user.is_superuser:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="У вас недостаточно прав.",
    )
