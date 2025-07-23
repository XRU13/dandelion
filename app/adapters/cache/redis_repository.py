"""
Redis репозиторий для кеширования пользовательских данных
"""
import json
import logging
import redis.asyncio as redis
import os

from typing import Any, Dict, List
from datetime import datetime, timezone

from app.application.entities import Event
from app.application.constants import CacheSettings, Limits, RedisConfig
from app.application.utils import EventTypeHelper

logger = logging.getLogger(__name__)


class RedisUserScoreRepository:
    """Репозиторий для работы с кешем Redis по счетам, событиям, достижениям и stats."""

    def __init__(self):
        redis_url = os.getenv("REDIS_URL", RedisConfig.DEFAULT_URL)
        self.redis = redis.from_url(redis_url, decode_responses=True)

    def _score_key(self, user_id: int) -> str:
        # "user:{user_id}:score"
        return CacheSettings.get_score_key(user_id)

    def _events_key(self, user_id: int) -> str:
        # "user:{user_id}:events"
        return CacheSettings.get_events_key(user_id)

    def _achievements_key(self, user_id: int) -> str:
        # "user:{user_id}:achievements"
        return CacheSettings.get_achievements_key(user_id)

    def _stats_key(self, user_id: int) -> str:
        # "user:{user_id}:stats"
        return CacheSettings.get_stats_key(user_id)

    async def get_score(self, user_id: int) -> int:
        """Получить общий счет пользователя из Redis."""
        try:
            val = await self.redis.get(self._score_key(user_id))
            return int(val) if val is not None else 0
        except Exception as e:
            logger.warning(f"Redis get_score error for user {user_id}: {e}")
            return 0

    async def set_score(self, user_id: int, score: int) -> None:
        """Установить итоговый счет пользователя в Redis (SET)."""
        try:
            await self.redis.set(
                self._score_key(user_id),
                score,
                ex=CacheSettings.DEFAULT_TTL
            )
            logger.debug(f"Set score={score} for user={user_id}")
        except Exception as e:
            logger.warning(f"Redis set_score error for user {user_id}: {e}")

    async def increment_score(self, user_id: int, points: int) -> int:
        """Атомарно увеличить счет пользователя на points (INCRBY)."""
        try:
            key = self._score_key(user_id)
            new_score = await self.redis.incrby(key, points)
            # обновляем TTL
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(
                f"Incremented score by {points} for user={user_id}, new={new_score}"
            )
            return new_score
        except Exception as e:
            logger.warning(f"Redis increment_score error for user {user_id}: {e}")
            # на ошибку – просто возвращаем начисленное
            return points

    async def add_event(self, user_id: int, event: Event) -> None:
        """Добавить событие в начало списка последних событий в Redis."""
        try:
            data = {
                "id": event.id,
                "event_type": EventTypeHelper.to_string(event.event_type),
                "details": event.details,
                "created_at": (event.created_at or datetime.now(timezone.utc)).isoformat()
            }
            key = self._events_key(user_id)
            await self.redis.lpush(key, json.dumps(data))
            # оставляем только Limits.EVENTS_IN_CACHE последних
            await self.redis.ltrim(key, 0, Limits.EVENTS_IN_CACHE - 1)
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(f"Added event {event.id} to cache for user {user_id}")
        except Exception as e:
            logger.warning(f"Redis add_event error for user {user_id}: {e}")

    async def get_events(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить кешированные последние события пользователя."""
        try:
            key = self._events_key(user_id)
            items = await self.redis.lrange(key, 0, -1)
            return [json.loads(it) for it in items]
        except Exception as e:
            logger.warning(f"Redis get_events error for user {user_id}: {e}")
            return []

    async def add_achievement(self, user_id: int, achievement_id: int) -> None:
        """Добавить идентификатор достижения в множество Redis."""
        try:
            key = self._achievements_key(user_id)
            await self.redis.sadd(key, achievement_id)
            await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
            logger.debug(f"Added achievement {achievement_id} to cache for user {user_id}")
        except Exception as e:
            logger.warning(f"Redis add_achievement error for user {user_id}: {e}")

    async def get_achievements(self, user_id: int) -> List[int]:
        """Получить список закешированных ID достижений пользователя."""
        try:
            key = self._achievements_key(user_id)
            items = await self.redis.smembers(key)
            return [int(i) for i in items]
        except Exception as e:
            logger.warning(f"Redis get_achievements error for user {user_id}: {e}")
            return []

    async def get_stats(self, user_id: int) -> Dict[str, Any] | None:
        """Получить кешированный ответ /stats/{user_id}."""
        try:
            key = self._stats_key(user_id)
            raw = await self.redis.get(key)
            return json.loads(raw) if raw else None
        except Exception as e:
            logger.warning(f"Redis get_stats error for user {user_id}: {e}")
            return None

    async def set_stats(self, user_id: int, stats: Dict[str, Any]) -> None:
        """Закешировать весь ответ /stats/{user_id} на TTL."""
        try:
            key = self._stats_key(user_id)
            await self.redis.set(key, json.dumps(stats), ex=CacheSettings.STATS_TTL)
            logger.debug(f"Cached stats for user={user_id}")
        except Exception as e:
            logger.warning(f"Redis set_stats error for user {user_id}: {e}")

