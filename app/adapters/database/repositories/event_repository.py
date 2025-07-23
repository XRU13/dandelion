from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.application.interfaces import IEventRepository
from app.application.entities import Event
from app.application.constants import Limits


class EventRepository(IEventRepository):
	"""Реализация репозитория событий на SQLAlchemy"""

	def __init__(self, session: AsyncSession):
		self.session = session

	async def create(self, event: Event) -> Event:
		self.session.add(event)
		await self.session.commit()
		await self.session.refresh(event)
		return event

	async def get_by_id(self, event_id: int) -> Event | None:
		result = await self.session.execute(
			select(Event).where(Event.id == event_id)
		)
		return result.scalar_one_or_none()

	async def get_by_user_id(self, user_id: int) -> list[Event]:
		result = await self.session.execute(
			select(Event).where(Event.user_id == user_id).order_by(
				Event.created_at.desc())
		)
		return list(result.scalars())

	async def get_recent_by_user_id(
		self,
		user_id: int,
		limit: int = Limits.RECENT_EVENTS_LIMIT,
	) -> list[Event]:
		result = await self.session.execute(
			select(Event).where(Event.user_id == user_id)
			.order_by(Event.created_at.desc())
			.limit(limit)
		)
		return list(result.scalars())
