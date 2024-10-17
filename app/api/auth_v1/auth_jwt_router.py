from app.api.auth_v1.auth_token_helpers import (
    create_access_token,
    create_refresh_token,
)
from app.api.auth_v1.validation_auth import (
    validate_auth_user,
)
from app.api.auth_v1.validation_auth_helper import get_current_auth_user_for_refresh
from app.core.schemas import user_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer,
)

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(prefix="/jwt", tags=["auth"], dependencies=[Depends(http_bearer)])


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: user_schemas.UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: user_schemas.UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user=user)
    return TokenInfo(
        access_token=access_token,
    )


# from fastapi import APIRouter, Depends, Response
# from sqlalchemy.ext.asyncio import AsyncSession
# from ...core.db.database import async_get_db
# from ...core.security import blacklist_token, oauth2_scheme
#
# router = APIRouter(tags=["login"])
#
#
# @router.post("/logout")
# async def logout(
#     response: Response,
#     access_token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(async_get_db),
# ) -> dict[str, str]:
#     try:
#         await blacklist_token(token=access_token, db=db)
#         response.delete_cookie(key="refresh_token")
#
#         return {"message": "Вы вышли из аккаунта."}
#
#     except InvalidTokenError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Неправильный токен.",
#         )
