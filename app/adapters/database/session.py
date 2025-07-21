import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.adapters.database.mapping import configure_mappers

# Настраиваем маппинг
configure_mappers()

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db'
)

# Создаем асинхронный движок
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов для отладки
    future=True
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    """Получить async сессию базы данных с автокоммитом"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 