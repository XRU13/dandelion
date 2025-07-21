import logging
from app.application.entities import Event, EventType, UserScore
from app.application.interfaces import (
	IUserRepository,
	IEventRepository,
	IUserScoreRepository,
)
from app.application.exceptions import (
	InvalidEventDataError,
	EventServiceError
)
from app.application.utils import (
	ScoreCalculator,
	ValidationHelper,
	UserValidator,
)
from app.adapters.celery.tasks import process_event as celery_process_event

logger = logging.getLogger(__name__)


class EventService:
	"""Сервис для работы с событиями"""

	def __init__(
		self,
		event_repo: IEventRepository,
		user_score_repo: IUserScoreRepository,
		user_repo: IUserRepository,
		redis_cache=None
	):
		self.event_repo = event_repo
		self.user_score_repo = user_score_repo
		self.user_repo = user_repo
		self.redis_cache = redis_cache

	async def process_event(
		self,
		user_id: int,
		event_type: EventType,
		details: dict | None = None,
	) -> Event:
		"""Обрабатывает событие пользователя"""
		if not ValidationHelper.validate_user_id(user_id=user_id):
			raise InvalidEventDataError(details="Некорректный ID пользователя")

		if not ValidationHelper.validate_event_details(details=details):
			raise InvalidEventDataError(details="Некорректные детали события")

		await UserValidator.ensure_user_exists(
			user_repo=self.user_repo,
			user_id=user_id,
		)

		try:
			event = Event(
				user_id=user_id,
				event_type=event_type,
				details=details
			)
			event = await self.event_repo.create(event=event)

			points_earned = await self._update_user_score(
				user_id=user_id,
				event_type=event_type,
			)
			await self._update_redis_cache(
				user_id=user_id,
				event=event,
				points_earned=points_earned,
			)

			# Запускаем Celery задачу process_event
			celery_process_event.delay(event.id)
			logger.debug(
				f"Triggered Celery process_event for event_id={event.id}")

			return event

		except Exception as e:
			raise EventServiceError(error=str(e))

	async def _update_redis_cache(
		self,
		user_id: int,
		event: Event,
		points_earned: int,
	) -> None:
		"""Обновляет кэш Redis с обработкой ошибок"""
		if not self.redis_cache:
			return

		try:
			await self.redis_cache.increment_score(
				user_id=user_id,
				points=points_earned,
			)
			await self.redis_cache.add_event(
				user_id=user_id,
				event=event,
			)
			logger.debug(
				f"Redis cache updated for user {user_id}: +{points_earned} points")
		except Exception as e:
			logger.warning(
				f"Failed to update Redis cache for user {user_id}: {e}")

	async def _update_user_score(
		self,
		user_id: int,
		event_type: EventType
	) -> int:
		"""Обновляет счет пользователя на основе события
		 и возвращает заработанные очки"""
		user_score = await self.user_score_repo.get_by_user_id(
			user_id=user_id
		)

		if not user_score:
			user_score = UserScore(
				user_id=user_id,
				login_count=0,
				levels_completed=0,
				secrets_found=0
			)
			user_score = await self.user_score_repo.create(
				user_score=user_score
			)

		ScoreCalculator.update_user_score_counters(
			user_score=user_score,
			event_type=event_type,
		)

		await self.user_score_repo.update(user_score=user_score)

		points_earned = ScoreCalculator.calculate_event_points(
			event_type=event_type
		)
		return points_earned
