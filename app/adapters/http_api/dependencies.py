"""
Dependency injection контейнер для всех сервисов и репозиториев.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.database.session import get_async_session
from app.adapters.database.repositories import (
	UserRepository,
	EventRepository,
	AchievementRepository,
	UserScoreRepository,
	UserAchievementRepository,
	AchievementNotificationRepository
)
from app.adapters.cache.redis_repository import RedisUserScoreRepository
from app.application.services.event_service import EventService
from app.application.services.achievement_service import AchievementService
from app.application.services.user_service import UserService
from app.application.services.stats_service import StatsService


def get_redis_repository() -> RedisUserScoreRepository:
	"""Фабрика для создания Redis кеша"""
	return RedisUserScoreRepository()


async def get_user_repository(
	session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
	"""Фабрика для создания репозитория пользователей"""
	return UserRepository(session)


async def get_event_repository(
	session: AsyncSession = Depends(get_async_session)
) -> EventRepository:
	"""Фабрика для создания репозитория событий"""
	return EventRepository(session)


async def get_achievement_repository(
	session: AsyncSession = Depends(get_async_session)
) -> AchievementRepository:
	"""Фабрика для создания репозитория достижений"""
	return AchievementRepository(session)


async def get_user_score_repository(
	session: AsyncSession = Depends(get_async_session)
) -> UserScoreRepository:
	"""Фабрика для создания репозитория счетов пользователей"""
	return UserScoreRepository(session)


async def get_user_achievement_repository(
	session: AsyncSession = Depends(get_async_session)
) -> UserAchievementRepository:
	"""Фабрика для создания репозитория достижений пользователей"""
	return UserAchievementRepository(session)


async def get_achievement_notification_repository(
	session: AsyncSession = Depends(get_async_session)
) -> AchievementNotificationRepository:
	"""Фабрика для создания репозитория уведомлений о достижениях"""
	return AchievementNotificationRepository(session)


async def get_user_service(
	user_repository: UserRepository = Depends(get_user_repository),
	user_score_repository: UserScoreRepository = Depends(
		get_user_score_repository)
) -> UserService:
	"""Фабрика для создания сервиса пользователей"""
	return UserService(user_repository, user_score_repository)


async def get_event_service(
	event_repository: EventRepository = Depends(get_event_repository),
	user_score_repository: UserScoreRepository = Depends(
		get_user_score_repository),
	user_repository: UserRepository = Depends(get_user_repository),
	redis_repository: RedisUserScoreRepository = Depends(get_redis_repository)
) -> EventService:
	"""Фабрика для создания сервиса событий"""
	return EventService(event_repository, user_score_repository,
	                    user_repository, redis_repository)


async def get_stats_service(
	user_repository: UserRepository = Depends(get_user_repository),
	user_score_repository: UserScoreRepository = Depends(
		get_user_score_repository),
	user_achievement_repository: UserAchievementRepository = Depends(
		get_user_achievement_repository),
	event_repository: EventRepository = Depends(get_event_repository),
	achievement_repository: AchievementRepository = Depends(
		get_achievement_repository),
	redis_repository: RedisUserScoreRepository = Depends(get_redis_repository)
) -> StatsService:
	"""Фабрика для создания сервиса статистики"""
	return StatsService(
		user_repository,
		user_score_repository,
		user_achievement_repository,
		event_repository,
		achievement_repository,
		redis_repository
	)


async def get_achievement_service(
	achievement_repository: AchievementRepository = Depends(
		get_achievement_repository),
	user_achievement_repository: UserAchievementRepository = Depends(
		get_user_achievement_repository),
	achievement_notification_repository: AchievementNotificationRepository = Depends(
		get_achievement_notification_repository),
	user_score_repository: UserScoreRepository = Depends(
		get_user_score_repository),
	redis_repository: RedisUserScoreRepository = Depends(get_redis_repository)
) -> AchievementService:
	"""Фабрика для создания сервиса достижений"""
	return AchievementService(
		achievement_repository,
		user_achievement_repository,
		achievement_notification_repository,
		user_score_repository,
		redis_repository
	)
