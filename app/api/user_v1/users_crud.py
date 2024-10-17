import uuid

from sqlalchemy import select

from app.core.models import user_model
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schemas import user_schemas
from app.auth import utils_jwt


class CRUDUser:
    async def get_user(self, db: AsyncSession, user_uuid: uuid.UUID):
        result = await db.execute(
            select(user_model.User).where(user_model.User.uuid == user_uuid)
        )
        return result.scalars().first()

    async def get_user_by_field(self, db: AsyncSession, field: str, value: str):
        if field == "email":
            result = await db.execute(
                select(user_model.User).where(user_model.User.email == value)
            )
            return result.scalars().first()

        if field == "username":
            result = await db.execute(
                select(user_model.User).where(user_model.User.username == value)
            )
            return result.scalars().first()
        if field == "phone_number":
            result = await db.execute(
                select(user_model.User).where(user_model.User.phone_number == value)
            )
            return result.scalars().first()

    async def create_user(self, db: AsyncSession, user: user_schemas.UserCreate):
        secret_password = utils_jwt.hash_password(user.password)
        db_user = user_model.User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            hashed_password=secret_password,
            email=user.email,
            phone_number=user.phone_number,
            is_active=False,
            is_superuser=False,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def update_user(
        self,
        db: AsyncSession,
        db_user: user_model.User,
        user_update: user_schemas.UserUpdate,
    ):
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def delete_user(self, db: AsyncSession, user_uuid: uuid.UUID):
        db_user = await self.get_user(db=db, user_uuid=user_uuid)
        if db_user:
            await db.delete(db_user)
            await db.commit()
            return {"message": "Пользователь успешно удален."}
        return db_user


crud_user = CRUDUser()
