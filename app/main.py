import os
import uvicorn
from dotenv import load_dotenv
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api import router as api_router
from app.admin_panel import views_admin
from app.admin_panel.auth_admin import authentication_backend
from app.middleware.superuser_middle import AdminAuthMiddleware
from core.config import settings
from create_fastapi_app import create_app
from sqladmin import Admin
from app.core.models import db_helper

load_dotenv()

# middleware = [
#     Middleware(SessionMiddleware, secret_key=os.getenv("FASTAPI__ADMIN__SECRET_KEY")),
#     Middleware(AdminAuthMiddleware),
# ]
main_app = create_app(
    create_custom_static_urls=True,  # Создание статических роутеров документации (Swagger)
)

admin = Admin(
    app=main_app,
    engine=db_helper.engine,
    authentication_backend=authentication_backend,
    base_url="/project_d_admin/",
    title="Административная панель",
)  # Инициализация панели администратора


for view in views_admin:
    admin.add_view(view)

main_app.include_router(api_router)  # Регистрация роутера API в основном приложении

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", reload=True, host=settings.run.host, port=settings.run.port
    )  # Запуск приложения на сервере
