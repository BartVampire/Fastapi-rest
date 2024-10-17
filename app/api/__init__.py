from fastapi import APIRouter
from .auth_v1 import auth_router
from .user_v1 import users_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(users_router, prefix="/user")
