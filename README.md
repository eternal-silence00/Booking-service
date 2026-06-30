# Сервис бронирования переговорных комнат

REST API для бронирования переговорных комнат в коворкинге. Сотрудники просматривают доступность комнат на дату, создают и отменяют свои бронирования; администраторы дополнительно могут отменять любые бронирования.

## Стек

- Python 3.12, FastAPI
- PostgreSQL + SQLAlchemy (async, asyncpg)
- Alembic (миграции)
- JWT-аутентификация (python-jose), bcrypt (passlib)
- Poetry (управление зависимостями)
- pytest (юнит- и интеграционные тесты)
- Docker, docker-compose

## Архитектура

Послойное разделение по доменам: роутер (HTTP) → сервис (бизнес-логика) → репозиторий (доступ к данным).

```
src/booking_service/
  core/        конфиг, подключение к БД, security (JWT, хеши, зависимости прав)
  users/       регистрация, аутентификация (модели, схемы, репозиторий, сервис, роутер)
  rooms/       комнаты и слоты
  bookings/    бронирования и доступность
  main.py      сборка приложения
alembic/       миграции
tests/         pytest
```

## Модель данных

- **User** — пользователь (email, пароль, роль `employee`/`admin`).
- **Room** — переговорная комната (название, вместимость).
- **Slot** — заранее заданный временной слот комнаты (`start_time`–`end_time`).
- **Booking** — бронирование слота на конкретную дату. Ограничение `UNIQUE(slot_id, booking_date)` на уровне БД гарантирует, что один слот нельзя забронировать дважды на одну дату (защита от пересечений).

## Эндпоинты

| Метод | Путь | Доступ | Описание |
|-------|------|--------|----------|
| POST | `/auth/register` | все | Регистрация (роль `employee`) |
| POST | `/auth/login` | все | Получение JWT по email/паролю |
| POST | `/rooms` | admin | Создать комнату |
| GET | `/rooms` | авторизованные | Список комнат |
| POST | `/rooms/{room_id}/slots` | admin | Добавить слот в комнату |
| GET | `/rooms/{room_id}/slots` | авторизованные | Слоты комнаты |
| GET | `/availability?date=YYYY-MM-DD` | авторизованные | Доступность всех комнат на дату |
| POST | `/bookings` | авторизованные | Создать бронирование |
| GET | `/bookings/me` | авторизованные | Свои бронирования |
| DELETE | `/bookings/{id}` | владелец или admin | Отменить бронирование |

Интерактивная документация (Swagger UI): `http://localhost:8000/docs`.

## Запуск через Docker (рекомендуется)

```bash
cp .env.example .env        # значения по умолчанию уже рабочие для Docker
docker compose up --build
```

Поднимутся PostgreSQL и приложение. Миграции применяются автоматически при старте. API доступен на `http://localhost:8000`.

## Локальный запуск

Требуется PostgreSQL на `localhost:5432`.

```bash
# 1. Создать базу
createdb -O postgres booking

# 2. Зависимости
poetry install

# 3. .env (DATABASE_URL должен указывать на localhost)
cp .env.example .env

# 4. Миграции
poetry run alembic upgrade head

# 5. Запуск
poetry run uvicorn booking_service.main:app --reload
```

## Тесты

Требуется тестовая база `booking_test`:

```bash
createdb -O postgres booking_test
poetry run pytest -v
```

Покрытие: регистрация и аутентификация, валидация, права доступа (admin/employee), создание и отмена бронирований, конфликт занятости, изоляция данных между пользователями, доступность по дате.

## Примеры работы

Регистрация и логин:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
# -> {"access_token": "...", "token_type": "bearer"}
```

Создание бронирования (с токеном):
```bash
curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"slot_id": 1, "booking_date": "2026-07-01"}'
```

Просмотр доступности:
```bash
curl "http://localhost:8000/availability?date=2026-07-01" \
  -H "Authorization: Bearer <access_token>"
```

## Назначение администратора

Регистрация создаёт пользователя с ролью `employee`. Чтобы назначить администратора, обновите роль в БД:

```bash
docker compose exec db psql -U postgres -d booking \
  -c "UPDATE users SET role='ADMIN' WHERE email='admin@example.com';"
```
