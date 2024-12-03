import os
from datetime import datetime, UTC, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.api.auth_v1.validation_auth import validate_auth_user
from app.api.user_v1.users_crud import crud_user
from app.api.auth_v1 import validation_auth, token_crud
from app.api.auth_v1.auth_jwt_router import auth_user_issue_jwt
from app.api.auth_v1.auth_token_helpers import create_access_token, create_refresh_token
from app.auth import decode_jwt
from app.core.models.db_helper import db_helper, DatabaseHelper


class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        secret_key: str,
        db_helper: DatabaseHelper,
        validate_auth_user,
        create_access_token,
        create_refresh_token,
        decode_jwt,
    ):
        super().__init__(secret_key)
        self.db_helper = db_helper
        self.validate_auth_user = validate_auth_user
        self.create_access_token = create_access_token
        self.create_refresh_token = create_refresh_token
        self.decode_jwt = decode_jwt

    async def login(self, request: Request) -> bool:
        try:
            form = await request.form()
            username, password = form["username"], form["password"]

            # Используем session_getter через async for
            async for db in self.db_helper.session_getter():
                # Используем существующую функцию валидации
                user = await self.validate_auth_user(
                    username=username, password=password, db=db
                )

                if not user:
                    return False

                # Создаем токены
                access_token = self.create_access_token(user=user)
                access_token = (
                    access_token.decode("utf-8")
                    if isinstance(access_token, bytes)
                    else access_token
                )
                # Сохраняем токены в сессии
                request.session.update(
                    {
                        "access_token": access_token,
                    }
                )

                return True
        except Exception as e:
            print(f"Ошибка входа: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        try:
            access_token = request.session.get("access_token")

            if access_token:
                async for db in self.db_helper.session_getter():
                    # Добавляем токены в черный список
                    access_token_bytes = access_token.encode("utf-8")

                    access_expires_at = datetime.fromtimestamp(
                        (self.decode_jwt(access_token_bytes)).get("exp")
                    )

                    username = request.session.get("username")

                    await token_crud.add_tokens_to_blacklist(
                        db=db,
                        access_token=access_token_bytes,
                        refresh_token=None,
                        access_expires_at=access_expires_at,
                        refresh_expires_at=None,
                        username=username,
                    )

            request.session.clear()
            return True
        except Exception as e:
            print(f"Выход из админ системы: {e}")
            return False

    async def authenticate(self, request: Request) -> bool:
        try:
            # Проверяем наличие токена в сессии
            access_token = request.session.get("access_token")
            if not access_token:
                return False

            # Проверяем валидность токена
            token_data = self.decode_jwt(access_token.encode("utf-8"))
            if not token_data:
                return False

            username = token_data.get("sub")
            async for db in self.db_helper.session_getter():
                check_superuser = await crud_user.get_user_by_field(
                    db=db,
                    field="username",
                    value=username,
                )
                if check_superuser.is_superuser is False:
                    return False

            # Проверяем не истек ли токен
            exp_timestamp = token_data.get("exp")
            if not exp_timestamp:
                return False

            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            if exp_datetime < datetime.now(UTC):
                return False

            return True
        except Exception as e:
            print(f"Ошибка авторизации в админ системе: {e}")
            return False


authentication_backend = AdminAuth(
    secret_key=os.getenv("FASTAPI__ADMIN__SECRET_KEY"),
    db_helper=db_helper,
    validate_auth_user=validate_auth_user,
    create_access_token=create_access_token,
    create_refresh_token=create_refresh_token,
    decode_jwt=decode_jwt,
)
