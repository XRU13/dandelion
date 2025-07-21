import os

from celery import Celery
from app.application.constants import CeleryConfig, RedisConfig

# Создаем экземпляр Celery
celery_app = Celery(
    "app",
    broker=os.getenv("REDIS_URL", RedisConfig.DEFAULT_URL),
    backend=os.getenv("REDIS_URL", RedisConfig.DEFAULT_URL)
)

# Конфигурация
celery_app.conf.update(
    result_expires=CeleryConfig.RESULT_EXPIRES,
    timezone="UTC",
    enable_utc=True,
)

# Автоматическое обнаружение задач
celery_app.autodiscover_tasks(["app.adapters.celery"]) 