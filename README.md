# 🎮 Gaming Achievement System

Современная система событий и достижений для игр, построенная на Clean Architecture с использованием FastAPI, PostgreSQL, Redis и Celery.

## 🚀 Особенности

- **Clean Architecture** - четкое разделение слоев (Application, Domain, Infrastructure)
- **Async/Await** - полностью асинхронная архитектура
- **Event-Driven** - обработка событий в реальном времени
- **Microservices Ready** - модульная структура для масштабирования
- **Production Ready** - Docker, мониторинг, логирование

## 📊 Функциональность

### События
- ✅ **Авторизация** (`login`) - 5 очков
- ✅ **Завершение уровня** (`complete_level`) - 20 очков  
- ✅ **Найден секрет** (`find_secret`) - 50 очков

### Достижения
- ✅ **Автоматическая проверка** условий
- ✅ **Уведомления** о получении
- ✅ **Система очков** за достижения

### Статистика
- ✅ **Общий счет** пользователя
- ✅ **Количество достижений**
- ✅ **Детальная статистика** по типам событий

## 🏗️ Архитектура

```
├── app/
│   ├── application/           # Бизнес-логика
│   │   ├── entities/         # Доменные сущности
│   │   ├── interfaces/       # Интерфейсы репозиториев
│   │   ├── services/         # Сервисы бизнес-логики
│   │   ├── constants.py      # Константы системы
│   │   ├── exceptions.py     # Типизированные исключения
│   │   └── utils.py          # Утилиты и хелперы
│   ├── adapters/             # Внешние адаптеры
│   │   ├── database/         # PostgreSQL + SQLAlchemy
│   │   ├── cache/            # Redis кэширование
│   │   ├── celery/           # Асинхронные задачи
│   │   └── http_api/         # FastAPI контроллеры
│   └── composites/           # Композиция зависимостей
```

## 🛠️ Технологический стек

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy 2.0** - ORM с async поддержкой
- **Alembic** - миграции базы данных
- **Pydantic 2.0** - валидация данных

### База данных
- **PostgreSQL** - основная БД
- **Redis** - кэширование и очереди

### Инфраструктура
- **Docker** + **Docker Compose**
- **Celery** - фоновые задачи
- **Flower** - мониторинг Celery
- **Gunicorn** + **Uvicorn** - ASGI сервер

## 🚀 Быстрый запуск

### Предварительные требования
- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)

### Запуск проекта
```bash
# Клонировать репозиторий
git clone https://github.com/XRU13/dandelion.git
cd dandelion

# Запустить все сервисы
docker-compose up -d

# Проверить работоспособность
curl http://localhost:8000/
```

### Проверка сервисов
- **API**: http://localhost:8000
- **Документация**: http://localhost:8000/docs
- **Flower** (Celery): http://localhost:5555
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📝 API Endpoints

### События
```bash
# Создать событие
POST /api/v1/event/
{
  "user_id": 1,
  "event_type": "login",
  "details": null
}

# Получить события пользователя
GET /api/v1/events/user/1
```

### Пользователи
```bash
# Получить пользователя
GET /api/v1/users/1

# Создать пользователя
POST /api/v1/users/
{
  "username": "player1", 
  "email": "player1@example.com"
}
```

### Достижения
```bash
# Все достижения
GET /api/v1/achievements/

# Достижения пользователя
GET /api/v1/achievements/users/1
```

### Статистика
```bash
# Статистика пользователя
GET /api/v1/stats/1
```

## 🔧 Разработка

### Локальная установка
```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить базу данных и Redis
docker-compose up -d postgres redis

# Применить миграции
cd app/adapters/database && alembic upgrade head

# Запустить сервер разработки
uvicorn app.composites.http_api:app --reload
```

### Работа с миграциями
```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

## 🧪 Тестирование

### Ручное тестирование
```bash
# Создать пользователя
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}'

# Создать событие входа (+5 очков)
curl -X POST http://localhost:8000/api/v1/event/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "event_type": "login"}'

# Проверить статистику
curl http://localhost:8000/api/v1/stats/1
```

### Мониторинг логов
```bash
# Логи приложения
docker logs fastapi_app -f

# Логи Celery worker
docker logs celery_worker -f

# Логи PostgreSQL
docker logs postgres_db -f
```

## 🎯 Константы и конфигурация

### Очки за события
```python
class EventPoints:
    LOGIN = 5           # Вход в игру
    COMPLETE_LEVEL = 20 # Завершение уровня
    FIND_SECRET = 50    # Найден секрет
```

### Настройки кэша
```python
class CacheSettings:
    DEFAULT_TTL = 3600  # 1 час
    SCORE_KEY_PREFIX = "user_score:"
    EVENT_KEY_PREFIX = "user_events:"
```

## 🛡️ Обработка ошибок

Система использует типизированные исключения с шаблонами сообщений:

```python
# Пример исключения
class UserNotFoundError(AppError):
    msg_template = 'Пользователь с ID {user_id} не найден'
    code = 'user_service.user_not_found'

# Использование
raise UserNotFoundError(user_id=123)
# → "Пользователь с ID 123 не найден"
```

## 📈 Мониторинг и метрики

### Логирование
- **Структурированные логи** для всех операций
- **Уровни важности**: DEBUG, INFO, WARNING, ERROR
- **Контекстная информация**: user_id, event_id, operation

### Health Checks
```bash
# Проверка API
curl http://localhost:8000/

# Проверка Redis
docker exec redis_cache redis-cli ping

# Проверка PostgreSQL
docker exec postgres_db pg_isready
```

## 🚀 Production Deployment

### Переменные окружения
```bash
# База данных
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379/0

# Настройки приложения
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

### Scaling
- **Horizontal**: множественные экземпляры FastAPI
- **Celery Workers**: масштабирование фоновых задач
- **Database**: read replicas для статистики
- **Redis**: Redis Cluster для высокой нагрузки

## 🔄 CI/CD

Проект готов для интеграции с:
- **GitHub Actions**
- **GitLab CI**
- **Jenkins**
- **Docker Hub** / **AWS ECR**

## 📞 Поддержка

При возникновении вопросов:
1. Проверьте логи сервисов
2. Убедитесь в работоспособности БД и Redis
3. Проверьте переменные окружения
4. Создайте Issue в репозитории

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

---

**Проект создан с использованием лучших практик Clean Architecture и готов к продакшену! 🎉** 