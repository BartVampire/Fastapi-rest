from datetime import datetime

from app.api.auth_v1.auth_helpers import (
    create_access_token,
    create_refresh_token,
)
from app.api.auth_v1.validation_auth import (
    get_current_token_payload,
    get_current_auth_user_for_refresh,
    get_current_active_auth_user,
    validate_auth_user,
)
from app.core.schemas import user_schemas
from fastapi import APIRouter, Depends
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


@router.get("/users/me")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: user_schemas.UserSchema = Depends(get_current_active_auth_user),
):
    iat_ts = datetime.fromtimestamp(timestamp=payload.get("iat"))
    iat = iat_ts.strftime("%H:%M:%S - %d.%m.%Y")
    return {
        "username": user.username,
        "email": user.email,
        "Дата входа": iat,
    }
