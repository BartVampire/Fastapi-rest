# 🍽️ Приложение Меню для Ресторанов на FastAPI

Добро пожаловать в **Приложение Меню для Ресторанов**! Это масштабируемое и универсальное приложение для управления меню нескольких ресторанов. Оно включает в себя аутентификацию на основе JWT, админ-панель, динамические веб-страницы и многое другое.

---

## 🚀 Возможности

- **Аутентификация на основе JWT**: Безопасная аутентификация с использованием access и refresh токенов.
- **Админ-панель**: Удобное управление данными через SQLAdmin.
- **PostgreSQL и Redis**: База данных и кэширование с использованием Docker Compose.
- **Миграции Alembic**: Простое управление схемой базы данных.
- **Шаблоны Jinja2**: Динамическая генерация веб-страниц для меню ресторанов.
- **Poetry**: Современное управление зависимостями.

---

## 🛠️ Инструкции по установке
### Предварительные требования
- Python 3.10+
- Docker и Docker Compose
- [Poetry](https://python-poetry.org/)

### 🐳 Запуск с использованием Docker Compose

1. **Склонируйте репозиторий**:
    ```bash
    git clone <ссылка_на_репозиторий>
    cd <название_репозитория>
    ```

2. **Создайте файл `.env`**:
   В директории `app` создайте файл `.env` со следующим содержимым:
    ```env
    FASTAPI__DB__URL=postgresql+asyncpg://postgres:<ваш_пароль>@db:5432/fastapi_db
    POSTGRES_HOST=db
    POSTGRES_PASSWORD=<ваш_пароль>
    FASTAPI__FIRST__PEPPER=<секрет_1>
    FASTAPI__SECOND__PEPPER=<секрет_2>
    FASTAPI__THIRD__PEPPER=<секрет_3>
    FASTAPI__ADMIN__SECRET_KEY=<секрет_для_админки>
    FASTAPI__REDIS__HOST=redis
    FASTAPI__REDIS__PORT=6379
    FASTAPI__REDIS__DB=0
    FASTAPI__REDIS__PASSWORD=<пароль_redis>
    ADMIN_USER_MODEL=app.models.User
    ADMIN_USER_MODEL_USERNAME_FIELD=username
    ADMIN_SECRET_KEY=<секрет_для_администратора>
    ```

3. **Запустите приложение**:
    ```bash
    docker-compose up --build
    ```

4. Откройте следующие сервисы:
    - **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Админ-панель**: [http://localhost:8000/project_d_admin](http://localhost:8000/project_d_admin)
    - **Меню ресторанов**: [http://localhost:8000/?restaurant_uuid=UUID]()
---

## 🗃️ Миграции базы данных

1. **Инициализация Alembic**:
    ```bash
    alembic init alembic
    ```

2. **Создание миграции**:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```

3. **Применение миграций**:
    ```bash
    alembic upgrade head
    ```

## 🛠️ Запуск в режиме разработки

1. **Установка зависимостей**:
    ```bash
    poetry install
    ```
2. **Запуск локально**:
    ```bash
    poetry poetry run uvicorn app.main:main_app --reload --host <ваш_хост> --port <ваш_порт>
    ```
---

## 🔧 Переменные окружения

| Название переменной              | Описание                                |
|----------------------------------|-----------------------------------------|
| `FASTAPI__DB__URL`               | URL подключения к базе данных           |
| `POSTGRES_HOST`                  | Хост PostgreSQL                         |
| `POSTGRES_PASSWORD`              | Пароль PostgreSQL                       |
| `FASTAPI__FIRST__PEPPER`         | Секретный ключ (pepper) для хэширования |
| `FASTAPI__SECOND__PEPPER`        | Секретный ключ (pepper) для хэширования |
| `FASTAPI__THIRD__PEPPER`         | Секретный ключ (pepper) для хэширования |
| `FASTAPI__ADMIN__SECRET_KEY`     | Секретный ключ для админки SQLADMIN     |
| `FASTAPI__REDIS__HOST`           | Хост Redis                              |
| `FASTAPI__REDIS__PORT`           | Порт Redis                              |
| `FASTAPI__REDIS__DB`             | Индекс базы Redis                       |
| `FASTAPI__REDIS__PASSWORD`       | Пароль Redis                            |
| `ADMIN_USER_MODEL`               | Путь к модели администратора            |
| `ADMIN_USER_MODEL_USERNAME_FIELD`| Поле имени пользователя в модели        |
| `ADMIN_SECRET_KEY`               | Секретный ключ администратора           |
