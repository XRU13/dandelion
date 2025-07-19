"""
Redis репозиторий для кеширования пользовательских данных
"""
import json
import logging
import redis.asyncio as redis
import os
from datetime import datetime
from app.application.entities import Event
from app.application.constants import CacheSettings

logger = logging.getLogger(__name__)


class RedisUserScoreRepository:
    """Репозиторий для кеширования счета пользователя в Redis"""
    
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    def _get_score_key(self, user_id: int) -> str:
        """Получить ключ для счета пользователя"""
        return f"{CacheSettings.SCORE_KEY_PREFIX}{user_id}"
    
    def _get_achievements_key(self, user_id: int) -> str:
        """Получить ключ для списка достижений пользователя"""
        return f"{CacheSettings.ACHIEVEMENT_KEY_PREFIX}{user_id}"
    
    def _get_events_key(self, user_id: int) -> str:
        """Получить ключ для последних событий пользователя"""
        return f"{CacheSettings.EVENT_KEY_PREFIX}{user_id}"
    
    # Основные методы для счета
    async def get_score(self, user_id: int) -> int:
        """Получить общий счет пользователя из Redis"""
        try:
            score = await self.redis.get(self._get_score_key(user_id))
            return int(score) if score else 0
        except Exception as e:
            logger.warning(f"Failed to get score from Redis for user {user_id}: {e}")
            return 0
    
    async def set_score(self, user_id: int, score: int) -> None:
        """Установить общий счет пользователя в Redis"""
        try:
            await self.redis.set(
                self._get_score_key(user_id), 
                score, 
                ex=CacheSettings.DEFAULT_TTL
            )
            logger.debug(f"Set score {score} for user {user_id} in Redis")
        except Exception as e:
            logger.warning(f"Failed to set score in Redis for user {user_id}: {e}")
    
    async def increment_score(self, user_id: int, points: int) -> int:
        """Увеличить счет пользователя на заданное количество очков"""
        try:
            key = self._get_score_key(user_id)
            new_score = await self.redis.incrby(key, points)
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(f"Incremented score by {points} for user {user_id}, new total: {new_score}")
            return new_score
        except Exception as e:
            logger.warning(f"Failed to increment score in Redis for user {user_id}: {e}")
            return points
    
    # Методы для событий
    async def add_event(self, user_id: int, event: Event) -> None:
        """Добавить событие в кеш пользователя"""
        try:
            event_data = {
                "id": event.id,
                "event_type": event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
                "details": event.details,
                "created_at": event.created_at.isoformat() if event.created_at else datetime.utcnow().isoformat()
            }
            
            key = self._get_events_key(user_id)
            await self.redis.lpush(key, json.dumps(event_data))
            # Оставляем только последние 10 событий
            await self.redis.ltrim(key, 0, 9)
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(f"Added event {event.id} to cache for user {user_id}")
        except Exception as e:
            logger.warning(f"Failed to add event to Redis for user {user_id}: {e}")
    
    async def get_recent_events(self, user_id: int, limit: int = 5) -> list[dict]:
        """Получить последние события пользователя"""
        try:
            key = self._get_events_key(user_id)
            events = await self.redis.lrange(key, 0, limit - 1)
            return [json.loads(event) for event in events]
        except Exception as e:
            logger.warning(f"Failed to get recent events from Redis for user {user_id}: {e}")
            return []
    
    # Методы для достижений
    async def add_achievement(self, user_id: int, achievement_id: int) -> None:
        """Добавить достижение в кеш пользователя"""
        try:
            key = self._get_achievements_key(user_id)
            await self.redis.sadd(key, achievement_id)
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(f"Added achievement {achievement_id} to cache for user {user_id}")
        except Exception as e:
            logger.warning(f"Failed to add achievement to Redis for user {user_id}: {e}")
    
    async def get_achievements_count(self, user_id: int) -> int:
        """Получить количество достижений пользователя"""
        try:
            count = await self.redis.scard(self._get_achievements_key(user_id))
            return count
        except Exception as e:
            logger.warning(f"Failed to get achievements count from Redis for user {user_id}: {e}")
            return 0
    
    async def has_achievement(self, user_id: int, achievement_id: int) -> bool:
        """Проверить есть ли достижение у пользователя в кеше"""
        try:
            key = self._get_achievements_key(user_id)
            return await self.redis.sismember(key, achievement_id)
        except Exception as e:
            logger.warning(f"Failed to check achievement in Redis for user {user_id}: {e}")
            return False
    
    # Утилитарные методы
    async def clear_user_cache(self, user_id: int) -> None:
        """Очистить весь кеш пользователя"""
        try:
            keys = [
                self._get_score_key(user_id),
                self._get_achievements_key(user_id),
                self._get_events_key(user_id)
            ]
            await self.redis.delete(*keys)
            logger.debug(f"Cleared cache for user {user_id}")
        except Exception as e:
            logger.warning(f"Failed to clear cache for user {user_id}: {e}")
    
    async def ping(self) -> bool:
        """Проверить доступность Redis"""
        try:
            await self.redis.ping()
            return True
        except Exception:
            return False
    
    async def close(self) -> None:
        """Закрыть соединение с Redis"""
        try:
            await self.redis.close()
            logger.debug("Redis connection closed")
        except Exception as e:
            logger.warning(f"Failed to close Redis connection: {e}")
    
    # Для обратной совместимости (deprecated методы)
    async def get_total_score(self, user_id: int) -> int:
        """Deprecated: используйте get_score()"""
        return await self.get_score(user_id)
    
    async def set_total_score(self, user_id: int, score: int) -> None:
        """Deprecated: используйте set_score()"""
        await self.set_score(user_id, score)
    
    async def add_last_event(self, user_id: int, event_data: dict) -> None:
        """Deprecated: используйте add_event()"""
        try:
            key = self._get_events_key(user_id)
            await self.redis.lpush(key, json.dumps(event_data))
            await self.redis.ltrim(key, 0, 4)
        except Exception:
            pass 