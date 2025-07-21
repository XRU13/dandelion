from abc import ABC, abstractmethod
from app.application.entities import Event
from app.application.constants import Limits


class IEventRepository(ABC):
    """Абстрактный репозиторий событий"""
    
    @abstractmethod
    async def create(self, event: Event) -> Event:
        pass
    
    @abstractmethod
    async def get_by_id(self, event_id: int) -> Event | None:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[Event]:
        pass
    
    @abstractmethod
    async def get_recent_by_user_id(
        self,
        user_id: int,
        limit: int = Limits.RECENT_EVENTS_LIMIT,
    ) -> list[Event]:
        pass
