from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfiguration(BaseModel):
    """
    Конфигурация запуска приложения
    """

    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    """
    Префикс для API
    """

    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    """
    Конфигурация базы данных
    """

    url: PostgresDsn
    echo: bool = False  # Логирование SQL-запросов в консоль
    echo_pool: bool = False  # Выводить логирование пула соединений
    pool_size: int = 50  # Размер количества соединений в пуле
    max_overflow: int = 10  # Количество превышения пула соединений

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }  # Правила именования таблиц в БД


class Settings(BaseSettings):
    """
    Настройки приложения
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # Имя файла с переменными окружения
        case_sensitive=False,  # Разрешить любой регистр в именах полей модели
        env_nested_delimiter="__",  # Разделитель для вложенных переменных окружения
        env_prefix="FASTAPI__",  # Префикс для переменных окружения
    )
    run: RunConfiguration = RunConfiguration()  # Конфигурация запуска приложения
    api: ApiPrefix = ApiPrefix()  # Конфигурация префикса для API
    db: DatabaseConfig


settings = Settings()
