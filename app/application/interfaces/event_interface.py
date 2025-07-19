from abc import ABC, abstractmethod


from ..entities import Event


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