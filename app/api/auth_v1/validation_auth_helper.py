import logging
from typing import Tuple

from fastapi import Depends, HTTPException, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.auth_v1.auth_utils import get_user_by_token_sub
from app.api.auth_v1.auth_token_helpers import (
    ACCESS_TOKEN_TYPE,
)
from fastapi.responses import RedirectResponse

from app.api.auth_v1.auth_utils import validate_token_type
from app.auth import utils_jwt
from app.auth.refresh_token_check import check_and_refresh_token_dependency
from app.core.models import db_helper
from app.core.schemas import user_schemas


logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


async def get_current_token_payload(
    # token: str | bytes = Depends(oauth2_scheme),
    access_token: Tuple[Request, str | bytes] = Depends(
        check_and_refresh_token_dependency
    ),
    refresh_token: str | bytes = Cookie(None),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> user_schemas.User | RedirectResponse:
    try:
        _, access_token = access_token
        print(f"access_token: get_current_token {access_token}")
        print(f"refresh_token: get_current_token {refresh_token}")
        if not access_token and not refresh_token:
            # Выбрасываем исключение, чтобы на уровне маршрута выполнить редирект
            raise HTTPException(
                status_code=status.HTTP_302_FOUND, detail="Пожалуйста, авторизуйтесь."
            )

        payload = utils_jwt.decode_jwt(token=access_token)
        print(f"payload: {payload}")
        return payload

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный токен.",
        )
    except Exception as e:
        logger.error(f"Неожиданная ошибка при проверке токена: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при проверке токена",
        )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> user_schemas.User:
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    return await get_user_by_token_sub(payload=payload, db=db)


async def get_current_active_auth_user(
    user: user_schemas.User = Depends(get_current_auth_user),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходимо зарегистрироваться.",
        )
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
