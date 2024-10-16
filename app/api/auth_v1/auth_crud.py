from app.auth import utils_jwt
from app.core.schemas import user_schemas

john = user_schemas.UserSchema(
    username="john",
    password=utils_jwt.hash_password("qwerty"),
    email="john@ex.com",
    active=True,
)
jane = user_schemas.UserSchema(
    username="jane",
    password=utils_jwt.hash_password("secret"),
    email="jane@ex.com",
    active=True,
)
users_db: dict[str, user_schemas.UserSchema] = {
    john.username: john,
    jane.username: jane,
}
