import os
import logging
import asyncio

from celery import Celery
from celery.signals import worker_ready, task_prerun, task_postrun, task_failure
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

logger = logging.getLogger(__name__)

# Настройка URL брокера и базы данных
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db'
)

# Инициализация Celery-приложения
celery_app = Celery(
    'app',
    broker=broker_url,
    backend=broker_url,
    include=['app.adapters.celery.tasks']
)
celery_app.conf.update(
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)

# Инициализация асинхронного движка и сессии для Celery-воркера
celery_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=5,
    max_overflow=10,
)
CelerySession = async_sessionmaker(
    celery_engine,
    expire_on_commit=False,
)

# Утилита для запуска async-корутины из sync-контекста Celery
# Движок и сессии создаются и уничтожаются в одном и том же event loop

def run_async(coro_func, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _wrapper():
        try:
            return await coro_func(CelerySession, *args, **kwargs)
        finally:
            # Закрываем все подключения после выполнения таска
            await celery_engine.dispose()

    try:
        return loop.run_until_complete(_wrapper())
    finally:
        asyncio.set_event_loop(None)
        loop.close()

# Сигналы для логирования жизненного цикла задач и воркера
@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    logger.info("Celery worker is ready")

@task_prerun.connect
def on_task_start(task_id, task, *args, **kwargs):
    logger.info(f"Task started: {task.name} [id={task_id}]")

@task_postrun.connect
def on_task_finish(task_id, task, retval, **kwargs):
    logger.info(f"Task finished: {task.name} [id={task_id}]")

@task_failure.connect
def on_task_failure(task_id, exception, traceback, task, **kwargs):
    logger.error(f"Task failure: {task.name} [id={task_id}], error: {exception}")
