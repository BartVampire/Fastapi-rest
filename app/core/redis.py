from functools import lru_cache

from fastapi import Depends
from redis import Redis, ConnectionPool
from typing import Optional
from .config import Settings
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    """Класс для работы с Redis"""

    _instance: Optional[Redis] = None  # Экземпляр клиента Redis
    _pool: Optional[ConnectionPool] = None  # Пул соединений с Redis

    @classmethod
    def init_pool(cls, settings: Settings) -> None:
        """Инициализация пула соединений"""
        if cls._pool is None:  # Проверка, инициализирован ли пул
            cls._pool = ConnectionPool(
                host=settings.redis.host,  # Хост Redis-сервера
                port=settings.redis.port,  # Порт Redis-сервера
                db=settings.redis.db,  # Номер базы данных Redis
                password=settings.redis.password,  # Пароль для подключения к Redis
                max_connections=settings.redis.max_connections,  # Максимальное количество соединений
                socket_timeout=settings.redis.socket_timeout,  # Таймаут сокета
                socket_connect_timeout=settings.redis.socket_connection_timeout,  # Таймаут соединения
                retry_on_timeout=settings.redis.retry_on_timeout,  # Повторять попытки при таймауте
                health_check_interval=settings.redis.health_check_interval,  # Интервал проверки состояния
            )
            print(f"Пул соединений с Redis успешно инициализирован ... :D")
            logger.info(
                f"Подключение к Redis успешно установлено: "
                f"host={settings.redis.host}, "
                f"port={settings.redis.port}, "
                f"db={settings.redis.db}"
            )

    @classmethod
    def get_client(cls, settings: Settings) -> Redis:
        """Получить клиент Redis"""
        if cls._instance is None:  # Проверка, создан ли экземпляр клиента
            if cls._pool is None:  # Если пул не инициализирован, инициализируем его
                cls.init_pool(settings)
            cls._instance = Redis(
                connection_pool=cls._pool, decode_responses=True
            )  # Создание клиента Redis
            # Проверка соединения
            try:
                cls._instance.ping()  # Проверка доступности Redis
                logger.info("Успешное подключение к Redis")
            except Exception as e:  # Обработка ошибок при подключении
                logger.error(f"Ошибка при подключении к Redis: {e}")
                raise  # Пробрасываем исключение дальше
        return cls._instance  # Возвращаем экземпляр клиента

    @classmethod
    def close(cls) -> None:
        """Закрыть соединение с Redis"""
        if cls._instance is not None:  # Проверка, существует ли экземпляр клиента
            cls._instance.close()  # Закрытие соединения с Redis
            cls._instance = None  # Обнуление экземпляра
        if cls._pool is not None:  # Проверка, существует ли пул соединений
            cls._pool.disconnect()  # Отключение пула соединений
            cls._pool = None  # Обнуление пула
        print(f"Закрытие соединения с Redis ... :D")
        logger.info("Закрытие соединения с Redis")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_redis(settings: Settings = Depends(get_settings)) -> Redis:
    return RedisClient.get_client(settings)
