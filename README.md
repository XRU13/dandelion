
#  Gaming Achievement System

Система игровых событий, достижений и подсчёта очков.  
Построена на **FastAPI + PostgreSQL + Redis + Celery**.

---

##  Быстрый запуск

```bash
docker-compose up --build
```

### Проверка:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Celery Flower: http://localhost:5555

---

##  Примеры запросов

###  Создать пользователя
```bash
curl -X POST http://localhost:8000/api/v1/users/   -H "Content-Type: application/json"   -d '{"username": "player1", "email": "player1@example.com"}'
```

###  Создать событие
```bash
curl -X POST http://localhost:8000/api/v1/event/   -H "Content-Type: application/json"   -d '{"user_id": 1, "event_type": "login"}'
```

###  Получить статистику пользователя
```bash
curl http://localhost:8000/api/v1/stats/1
```

---

## ️ Атомарность

- Все изменения в счёте и достижениях обрабатываются в рамках одной транзакции SQLAlchemy.
- В случае ошибки выполняется **session.rollback()**.
- Обновление счёта в Redis через атомарную команду **INCRBY**.
- Кэш в Redis обновляется только после успешного коммита в БД.
- Celery задачи работают независимо и не влияют на целостность данных в БД.

---

##  Технологии

- Python 3.11
- FastAPI
- PostgreSQL
- Redis
- Celery
- SQLAlchemy (async)
- Docker + Docker Compose

---

##  Поддержка и диагностика

### Логи приложения:
```bash
docker logs fastapi_app -f
```

### Логи Celery Worker:
```bash
docker logs celery_worker -f
```

### Проверка Redis:
```bash
docker exec redis_cache redis-cli ping
```

### Проверка PostgreSQL:
```bash
docker exec postgres_db pg_isready
```
