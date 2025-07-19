from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



from app.application.interfaces import IEventRepository
from app.application.entities import Event


class EventRepository(IEventRepository):
    """Реализация репозитория событий на SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, event: Event) -> Event:
        self.session.add(event)
        return event
    
    async def get_by_id(self, event_id: int) -> Event | None:
        result = await self.session.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> list[Event]:
        result = await self.session.execute(
            select(Event).where(Event.user_id == user_id).order_by(Event.created_at.desc())
        )
        return list(result.scalars()) 