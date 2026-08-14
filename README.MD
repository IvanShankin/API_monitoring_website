# API Monitoring Service

Backend-сервис для мониторинга доступности веб-сайтов и сбора статистики HTTP-проверок.

Сервис позволяет пользователям добавлять сайты для мониторинга, настраивать интервал и таймаут проверки, а также получать историю результатов проверок.

Проверки выполняются асинхронно в фоне с помощью **Celery**, **RabbitMQ** и **Redis**.

## Возможности

* Регистрация и аутентификация пользователей
* JWT Access/Refresh Tokens
* Добавление и управление сайтами для мониторинга
* Настройка интервала проверки сайта
* Настройка timeout для HTTP-запросов
* Периодическая автоматическая проверка сайтов
* Параллельная проверка нескольких сайтов
* Сохранение результатов каждой проверки
* Сбор HTTP status code и времени ответа
* Определение типов ошибок:
  * connection error
  * timeout
  * HTTP error
  * invalid URL
  * protocol error
  * decoding error и др.
* Получение истории проверок
* Удаление отдельных или всех проверок сайта
* Асинхронная работа с PostgreSQL
* Миграции базы данных через Alembic
* Docker Compose для запуска всей инфраструктуры
* Набор unit/integration-тестов

## Стек

### Backend

* **Python 3.13**
* **FastAPI**
* **SQLAlchemy 2.0**
* **Pydantic 2**
* **asyncio**
* **httpx**

### Database

* **PostgreSQL 15**
* **asyncpg**
* **Alembic**

### Background Tasks

* **Celery**
* **RabbitMQ**
* **Redis**

### Authentication

* JWT
* Access Token
* Refresh Token
* bcrypt

### Testing

* pytest
* pytest-asyncio
* httpx

### Infrastructure

* Docker
* Docker Compose
* Uvicorn

## Архитектура

Основной backend построен вокруг FastAPI.

Периодические проверки работают следующим образом:

```text
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    └──────────────┘
                           ▲
                           │
                    ┌──────┴───────┐
                    │    Celery    │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │   RabbitMQ  │           │    Redis    │
       └─────────────┘           └─────────────┘
              │
              ▼
       ┌─────────────────┐
       │ Website Monitor │
       └────────┬────────┘
                │
                ▼
          HTTP-запросы
                │
                ▼
        ┌───────────────┐
        │ Website Check │
        └───────────────┘
```

`Celery Beat` каждые 5 секунд запускает задачу планирования проверок.

Планировщик получает активные сайты из PostgreSQL, разбивает их на batch'и и отправляет задачи в Celery.

Каждый worker параллельно выполняет HTTP-проверки и сохраняет результаты в PostgreSQL.

## API

После запуска документация Swagger доступна по адресу:

```text
http://localhost:8021/docs
```

### Authentication

| Method | Endpoint               | Description        |
| ------ | ---------------------- | ------------------ |
| POST   | `/auth/register`       | Регистрация        |
| POST   | `/auth/login`          | Авторизация        |
| POST   | `/auth/refresh_tokens` | Обновление токенов |
| POST   | `/auth/logout`         | Выход              |

### Users

| Method | Endpoint    | Description                    |
| ------ | ----------- | ------------------------------ |
| GET    | `/users/me` | Получить текущего пользователя |

### Websites

| Method | Endpoint                 | Description         |
| ------ | ------------------------ | ------------------- |
| POST   | `/websites`              | Добавить сайт       |
| GET    | `/websites`              | Получить свои сайты |
| GET    | `/websites/{website_id}` | Получить сайт       |
| PUT    | `/websites/{website_id}` | Обновить сайт       |
| DELETE | `/websites`              | Удалить сайты       |

### Website checks

| Method | Endpoint                        | Description            |
| ------ | ------------------------------- | ---------------------- |
| GET    | `/website_check/{check_id}`     | Получить проверку      |
| GET    | `/websites/{website_id}/checks` | История проверок сайта |
| DELETE | `/website_check`                | Удалить проверки       |
| DELETE | `/websites/{website_id}/checks` | Удалить историю сайта  |

## Быстрый запуск через Docker

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd API_monitoring_website
```

### 2. Создать файл окружения

Для Docker используется `.dev.env`.

При необходимости создайте его на основе `.env.example`:

```bash
cp .env.example .dev.env
```

### 3. Запустить инфраструктуру

```bash
docker compose up --build
```

### 4. Выполнить миграции

После запуска контейнеров:

```bash
docker exec -it backend_monitoring alembic upgrade head
```

### 5. Открыть Swagger

```text
http://localhost:8021/docs
```

## Тестирование

Запуск всех тестов:

```bash
pytest
```

## Мониторинг сайтов

Для каждой проверки сохраняется:

* HTTP status code
* время ответа в миллисекундах
* доступность сайта
* время проверки
* тип ошибки
* сообщение об ошибке

Пример результата успешной проверки:

```json
{
    "website_id": 1,
    "http_status_code": 200,
    "response_time_ms": 143,
    "is_available": true
}
```

При ошибке:

```json
{
    "website_id": 1,
    "http_status_code": null,
    "response_time_ms": 5000,
    "is_available": false,
    "error_type": "read_timeout",
    "error_message": "Таймаут ожидания ответа"
}
```

Проверки выполняются асинхронно. Для ограничения количества одновременно выполняемых HTTP-запросов используется `asyncio.Semaphore`.

## Docker-сервисы

| Service              |    Port | Назначение             |
| -------------------- | ------: | ---------------------- |
| `backend_monitoring` |  `8021` | FastAPI                |
| `postgres`           |  `5432` | PostgreSQL             |
| `redis`              |  `6379` | Redis                  |
| `rabbitmq`           |  `5672` | Message broker         |
| `rabbitmq`           | `15672` | RabbitMQ Management UI |

RabbitMQ Management UI:

```text
http://localhost:15672
```

Стандартные credentials для локального запуска:

```text
login: guest
password: guest
```

## Основной сценарий работы

```text
1. Пользователь регистрируется
          ↓
2. Получает JWT-токены
          ↓
3. Добавляет сайт
          ↓
4. Celery Beat запускает планировщик
          ↓
5. Планировщик выбирает сайты для проверки
          ↓
6. Celery распределяет задачи между workers
          ↓
7. Worker выполняет HTTP-запрос
          ↓
8. Результат сохраняется в PostgreSQL
          ↓
9. Пользователь получает историю проверок через API
```
Задание получено с :solvit.space/projects/uptime_monitor
