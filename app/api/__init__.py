from fastapi import APIRouter
from .auth_v1 import auth_router
from .user_v1 import users_router
from .tier_v1 import tier_router
from .restaurant_v1 import restaurant_router
from .portions_v1 import portions_router
from .category_v1 import category_router
from .products_v1 import products_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(users_router, prefix="/user")

router.include_router(tier_router, prefix="/tier")
router.include_router(restaurant_router, prefix="/restaurant")

router.include_router(portions_router, prefix="/portions")
router.include_router(category_router, prefix="/categories")
router.include_router(products_router, prefix="/products")
