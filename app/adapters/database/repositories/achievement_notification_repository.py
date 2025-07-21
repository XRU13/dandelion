from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.application.interfaces import IAchievementNotificationRepository
from app.application.entities import AchievementNotification


class AchievementNotificationRepository(IAchievementNotificationRepository):
    """Реализация репозитория уведомлений о достижениях"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
	    self,
	    notification: AchievementNotification,
    ) -> AchievementNotification:
        self.session.add(notification)
        return notification

    async def mark_as_sent(self, notification_id: int) -> None:
        await self.session.execute(
            update(AchievementNotification)
            .where(AchievementNotification.id == notification_id)
            .values(is_sent=True)
        )