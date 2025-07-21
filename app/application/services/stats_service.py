import json

from app.application.interfaces import (
	IUserRepository,
	IUserScoreRepository,
	IUserAchievementRepository,
	IEventRepository,
	IAchievementRepository,
)
from app.application.constants import Limits
from app.application.exceptions import StatsServiceError
from app.application.utils import UserValidator, EventTypeHelper
from app.application.constants import CacheSettings


class StatsService:
	"""Сервис для работы со статистикой пользователей"""

	def __init__(
		self,
		user_repo: IUserRepository,
		user_score_repo: IUserScoreRepository,
		user_achievement_repo: IUserAchievementRepository,
		event_repo: IEventRepository,
		achievement_repo: IAchievementRepository,
		redis_cache=None
	):
		self.user_repo = user_repo
		self.user_score_repo = user_score_repo
		self.user_achievement_repo = user_achievement_repo
		self.event_repo = event_repo
		self.achievement_repo = achievement_repo
		self.redis_cache = redis_cache

	async def get_user_stats(self, user_id: int) -> dict:
		"""Получить полную статистику пользователя с кешированием"""
		await UserValidator.ensure_user_exists(
			user_repo=self.user_repo,
			user_id=user_id,
		)

		cache_key = CacheSettings.get_stats_key(user_id=user_id)

		# Пытаемся получить из кеша весь ответ
		if self.redis_cache:
			cached_data = await self.redis_cache.redis.get(cache_key)
			if cached_data:
				return json.loads(cached_data)

		try:
			score = 0
			if self.redis_cache:
				try:
					score = await self.redis_cache.get_score(user_id=user_id)
				except Exception:
					pass

			user_achievements = await self.user_achievement_repo.get_by_user_id(
				user_id=user_id
			)
			achievement_names = []
			for user_achievement in user_achievements:
				achievement = await self.achievement_repo.get_by_id(
					achievement_id=user_achievement.achievement_id
				)
				if achievement:
					achievement_names.append(achievement.name)

			last_events = await self.event_repo.get_recent_by_user_id(
				user_id=user_id,
				limit=Limits.RECENT_EVENTS_LIMIT,
			)

			stats_data = {
				"user_id": user_id,
				"score": score,
				"achievements": achievement_names,
				"last_events": [
					{
						"id": event.id,
						"event_type": EventTypeHelper.to_string(
							event.event_type),
						"details": event.details,
						"created_at": event.created_at.isoformat()
					}
					for event in last_events
				]
			}

			# Сохраняем в Redis целиком
			if self.redis_cache:
				await self.redis_cache.redis.set(
					cache_key,
					json.dumps(stats_data),
					ex=CacheSettings.STATS_TTL
				)

			return stats_data

		except Exception as e:
			raise StatsServiceError(error=str(e))
