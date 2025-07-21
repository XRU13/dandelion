import asyncio
import logging
from app.adapters.celery.config import celery_app
from app.adapters.database.session import AsyncSessionLocal
from app.adapters.database.repositories import (
	EventRepository,
	UserScoreRepository,
	AchievementRepository,
	UserAchievementRepository,
	AchievementNotificationRepository
)
from app.adapters.cache.redis_repository import RedisUserScoreRepository
from app.application.entities import (
	UserScore,
	UserAchievement,
	AchievementNotification,
)
from app.application.utils import ScoreCalculator, AchievementChecker
from app.application.constants import Messages

logger = logging.getLogger(__name__)


@celery_app.task(name="send_achievement_notification")
def send_achievement_notification(user_id: int, achievement_id: int):
	async def _send_notification():
		try:
			logger.info(
				f"Sending achievement notification for user {user_id}, achievement {achievement_id}")

			async with AsyncSessionLocal() as session:
				achievement_repo = AchievementRepository(session=session)
				notification_repo = AchievementNotificationRepository(
					session=session)

				achievement = await achievement_repo.get_by_id(
					achievement_id=achievement_id)
				if not achievement:
					logger.warning(f"Achievement {achievement_id} not found")
					return f"Achievement {achievement_id} not found"

				notification = AchievementNotification(
					user_id=user_id,
					achievement_id=achievement_id,
					message=f"Поздравляем! Вы получили достижение: {achievement.name}"
				)

				await notification_repo.create(notification)
				await session.commit()

				logger.info(
					f"[Achievement] User #{user_id} unlocked '{achievement.name}'")

				await notification_repo.mark_as_sent(notification.id)
				await session.commit()

				return f"Notification sent for achievement: {achievement.name}"

		except Exception as e:
			logger.error(
				f"Error sending notification for user {user_id}, achievement {achievement_id}: {e}",
				exc_info=True)
			return str(e)

	return asyncio.run(_send_notification())


@celery_app.task(name="process_event")
def process_event(event_id: int):
	async def _process_event():
		try:
			logger.info(f"Processing event {event_id}")

			async with AsyncSessionLocal() as session:
				event_repo = EventRepository(session)
				user_score_repo = UserScoreRepository(session)
				achievement_repo = AchievementRepository(session)
				user_achievement_repo = UserAchievementRepository(session)
				redis_cache = RedisUserScoreRepository()

				event = await event_repo.get_by_id(event_id)
				if not event:
					logger.warning(f"Событие {event_id} не найдено")
					return f"Событие {event_id} не найдено"

				points = ScoreCalculator.calculate_event_points(
					event_type=event.event_type,
					details=event.details,
				)

				user_score = await user_score_repo.get_by_user_id(event.user_id)
				if not user_score:
					user_score = UserScore(
						user_id=event.user_id,
						login_count=0,
						levels_completed=0,
						secrets_found=0
					)
					user_score = await user_score_repo.create(user_score)

				total_score = ScoreCalculator.calculate_total_score(user_score)

				all_achievements = await achievement_repo.get_all()
				user_achievements = await user_achievement_repo.get_by_user_id(
					event.user_id)
				earned_achievement_ids = AchievementChecker.get_earned_achievement_ids(
					user_achievements)

				new_achievements = []
				for achievement in all_achievements:
					if achievement.id in earned_achievement_ids:
						continue

					if AchievementChecker.check_achievement_condition(
						achievement, user_score):
						user_achievement = UserAchievement(
							user_id=event.user_id,
							achievement_id=achievement.id
						)
						await user_achievement_repo.create(user_achievement)
						new_achievements.append(achievement)

						logger.info(f"Earned achievement: {achievement.name}")

						loop = asyncio.get_running_loop()
						loop.call_soon_threadsafe(
							send_achievement_notification.delay,
							event.user_id,
							achievement.id
						)

				try:
					await redis_cache.set_score(event.user_id, total_score)
					await redis_cache.add_event(event.user_id, event)
					for achievement in new_achievements:
						await redis_cache.add_achievement(event.user_id,
						                                  achievement.id)

				except Exception as redis_error:
					logger.warning(
						f"Failed to update Redis cache: {redis_error}")

				await session.commit()

				result = Messages.EVENT_PROCESSING_SUCCESS.format(
					event_id=event_id,
					points=points,
					total_score=total_score
				)
				if new_achievements:
					achievement_names = [a.name for a in new_achievements]
					result += f", new achievements: {', '.join(achievement_names)}"

				logger.info(result)
				return result

		except Exception as e:
			logger.error(
				Messages.EVENT_PROCESSING_ERROR.format(event_id=event_id,
				                                       error=str(e)),
				exc_info=True)
			return str(e)

	return asyncio.run(_process_event())
