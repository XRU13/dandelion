"""
Redis репозиторий для кеширования пользовательских данных
"""
import json
import logging
import redis.asyncio as redis
import os

from datetime import datetime, timezone
from app.application.entities import Event
from app.application.constants import CacheSettings, Limits, RedisConfig
from app.application.utils import EventTypeHelper

logger = logging.getLogger(__name__)


class RedisUserScoreRepository:
	"""Репозиторий для кеширования счета пользователя в Redis"""

	def __init__(self):
		redis_url = os.getenv("REDIS_URL", RedisConfig.DEFAULT_URL)
		self.redis = redis.from_url(redis_url, decode_responses=True)

	def _get_score_key(self, user_id: int) -> str:
		"""Получить ключ для счета пользователя: user:{user_id}:score"""
		return CacheSettings.get_score_key(user_id)

	def _get_achievements_key(self, user_id: int) -> str:
		"""Получить ключ для списка достижений пользователя"""
		return CacheSettings.get_achievements_key(user_id)

	def _get_events_key(self, user_id: int) -> str:
		"""Получить ключ для последних событий пользователя"""
		return CacheSettings.get_events_key(user_id)

	# Основные методы для счета
	async def get_score(self, user_id: int) -> int:
		"""Получить общий счет пользователя из Redis"""
		try:
			score = await self.redis.get(self._get_score_key(user_id))
			return int(score) if score else 0
		except Exception as e:
			logger.warning(
				f"Failed to get score from Redis for user {user_id}: {e}")
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
			logger.warning(
				f"Failed to set score in Redis for user {user_id}: {e}")

	async def increment_score(self, user_id: int, points: int) -> int:
		"""Увеличить счет пользователя на заданное количество очков"""
		try:
			key = self._get_score_key(user_id)
			new_score = await self.redis.incrby(key, points)
			await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
			logger.debug(
				f"Incremented score by {points} for user {user_id}, new total: {new_score}")
			return new_score
		except Exception as e:
			logger.warning(
				f"Failed to increment score in Redis for user {user_id}: {e}")
			return points

	# Методы для событий
	async def add_event(self, user_id: int, event: Event) -> None:
		"""Добавить событие в кеш пользователя"""
		try:
			event_data = {
				"id": event.id,
				"event_type": EventTypeHelper.to_string(event.event_type),
				"details": event.details,
				"created_at": event.created_at.isoformat() if (
					event.created_at
				) else datetime.now(timezone.utc).isoformat()
			}

			key = self._get_events_key(user_id)
			await self.redis.lpush(key, json.dumps(event_data))
			# Оставляем только последние события согласно лимиту
			await self.redis.ltrim(key, 0, Limits.EVENTS_IN_CACHE - 1)
			await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
			logger.debug(f"Added event {event.id} to cache for user {user_id}")
		except Exception as e:
			logger.warning(
				f"Failed to add event to Redis for user {user_id}: {e}")

	# Методы для достижений
	async def add_achievement(self, user_id: int, achievement_id: int) -> None:
		"""Добавить достижение в кеш пользователя"""
		try:
			key = self._get_achievements_key(user_id)
			await self.redis.sadd(key, achievement_id)
			await self.redis.expire(key, CacheSettings.DEFAULT_TTL)
			logger.debug(
				f"Added achievement {achievement_id} to cache for user {user_id}")
		except Exception as e:
			logger.warning(
				f"Failed to add achievement to Redis for user {user_id}: {e}")
