from celery import Celery
import os

# Создаем экземпляр Celery
celery_app = Celery(
    "app",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# Конфигурация
celery_app.conf.update(
    result_expires=3600,
    timezone="UTC",
    enable_utc=True,
    include=["app.adapters.celery.tasks"]
)

# Автоматическое обнаружение задач
celery_app.autodiscover_tasks(["app.adapters.celery"]) 