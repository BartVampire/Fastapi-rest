import uuid as uuid_pkg
import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models import BaseModel
from .mixins.id_int_pk import IdIntPrimaryKeyMixin


class User(IdIntPrimaryKeyMixin, BaseModel):
    """
    Класс User представляет собой модель пользователя в базе данных. Он наследует от IdIntPrimaryKeyMixin и BaseModel.
    Поля класса:

    .first_name: Mapped[str] - Имя пользователя. Строка длиной до 30 символов.
    .last_name: Mapped[str] - Фамилия пользователя. Строка длиной до 30 символов.
    .username: Mapped[str] - Уникальное имя пользователя. Строка длиной до 50 символов. Поле индексируется для ускорения поиска.
    .email: Mapped[str] - Уникальный адрес электронной почты пользователя. Строка длиной до 50 символов. Поле индексируется для ускорения поиска.
    .phone_number: Mapped[str] - Уникальный номер телефона пользователя. Строка длиной до 25 символов. Поле индексируется для ускорения поиска.
    .hashed_password: Mapped[str] - Хэшированный пароль пользователя. Длина не ограничена.
    .uuid: Mapped[uuid_pkg.UUID] - Уникальный идентификатор пользователя в формате UUID. Генерируется автоматически с помощью uuid4.
    .created_at: Mapped[datetime.datetime] - Дата и время создания записи пользователя. Устанавливается автоматически на текущее время в формате UTC при создании записи.
    .updated_at: Mapped[datetime.datetime | None] - Дата и время последнего обновления записи пользователя. По умолчанию None, что означает, что значение не установлено при создании.
    .deleted_at: Mapped[datetime.datetime | None] - Дата и время, когда запись была помечена как удаленная. По умолчанию None, что означает, что запись не удалена.
    .is_deleted: Mapped[bool] - Логическое значение, указывающее, была ли запись удалена. По умолчанию False. Поле индексируется для ускорения поиска удаленных записей.
    .is_active: Mapped[bool]- Логическое значение, указывающее, подтвержден ли пользователь. По умолчанию False. Поле индексируется для ускорения поиска.
    .is_superuser: Mapped[bool] - Логическое значение, указывающее, является ли пользователь суперпользователем. По умолчанию False.
    .tier_id: Mapped[int | None] - Идентификатор уровня доступа пользователя, который ссылается на другую таблицу tier. Это поле может быть None, если у пользователя нет уровня доступа. Поле индексируется для ускорения поиска.
    """

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default_factory=lambda: datetime.UTC,
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, default=None)
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    tier_id: Mapped[int | None] = mapped_column(
        ForeignKey("tier.id"),
        index=True,
        default=None,
    )
