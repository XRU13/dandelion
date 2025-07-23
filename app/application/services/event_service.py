import logging
from app.application.entities import Event, EventType
from app.application.interfaces import (
	IUserRepository,
	IEventRepository,
)
from app.application.exceptions import (
	InvalidEventDataError,
	EventServiceError
)
from app.application.utils import (
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
		user_repo: IUserRepository,
	):
		self.event_repo = event_repo
		self.user_repo = user_repo

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

			celery_process_event.delay(event.id)

			return event

		except Exception as e:
			raise EventServiceError(error=str(e)) from e
