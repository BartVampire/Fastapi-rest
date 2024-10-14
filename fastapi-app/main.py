import uvicorn
from api import router as api_router
from core.config import settings
from create_fastapi_app import create_app


main_app = create_app(
    create_custom_static_urls=True  # Создание статических роутеров документации (Swagger)
)
main_app.include_router(api_router)  # Регистрация роутера API в основном приложении

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", reload=True, host=settings.run.host, port=settings.run.port
    )  # Запуск приложения на сервере
