from abc import ABC, abstractmethod
from ..entities import AchievementNotification


class IAchievementNotificationRepository(ABC):
    """Абстрактный репозиторий уведомлений о достижениях"""
    
    @abstractmethod
    async def create(self, notification: AchievementNotification) -> AchievementNotification:
        pass
    
    @abstractmethod
    async def get_unsent(self) -> list[AchievementNotification]:
        pass
    
    @abstractmethod
    async def mark_as_sent(self, notification_id: int) -> None:
        pass 