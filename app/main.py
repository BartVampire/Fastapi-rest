import os
import uvicorn
from dotenv import load_dotenv
from fastadmin.api.frameworks.fastapi.api import export
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from api import router as api_router
from app.admin_panel import views_admin
from app.admin_panel.auth_admin import authentication_backend
from app.fastadmin_panel import UserAdmin
from app.flask_adminka.app import create_flask_app
from core.config import settings
from create_fastapi_app import create_app
from sqladmin import Admin
from app.core.models import db_helper
from app.jinja2_main import router as jinja2_router
from fastapi.staticfiles import StaticFiles
from fastadmin import fastapi_app as admin_app, register_admin_model_class
from app.core.models.user_model import User
from fastadmin.models.helpers import admin_models

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

# Получаем абсолютный путь к директории статических файлов и медиа
static_dir = os.path.join(os.path.dirname(__file__), "static")
media_dir = os.path.join(os.path.dirname(__file__), "media")

main_app.mount(
    "/static", StaticFiles(directory=static_dir), name="static"
)  # Регистрация директории статических файлов

main_app.mount("/media", StaticFiles(directory=media_dir), name="media")
for view in views_admin:
    admin.add_view(view)

# admin_flask = create_flask_app(app=main_app, db=db_helper.get_sync_session())
# main_app.mount("/admins", WSGIMiddleware(admin_flask))

# main_app.mount(path="/admin", app=admin_app)

main_app.include_router(api_router)  # Регистрация роутера API в основном приложении
main_app.include_router(
    jinja2_router
)  # Регистрация роутера Jinja2 API в основном приложении

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", reload=True, host=settings.run.host, port=settings.run.port
    )  # Запуск приложения на сервере
