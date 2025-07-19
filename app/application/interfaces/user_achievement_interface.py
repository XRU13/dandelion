from abc import ABC, abstractmethod
from ..entities import UserAchievement


class IUserAchievementRepository(ABC):
    """Абстрактный репозиторий достижений пользователей"""
    
    @abstractmethod
    async def create(self, user_achievement: UserAchievement) -> UserAchievement:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[UserAchievement]:
        pass
    
    @abstractmethod
    async def exists(self, user_id: int, achievement_id: int) -> bool:
        pass 