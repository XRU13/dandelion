from abc import ABC, abstractmethod


from ..entities import Achievement


class IAchievementRepository(ABC):
    """Абстрактный репозиторий достижений"""
    
    @abstractmethod
    async def get_all(self) -> list[Achievement]:
        pass
    
    @abstractmethod
    async def get_by_id(self, achievement_id: int) -> int | None:
        pass 