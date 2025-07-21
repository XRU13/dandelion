from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.application.interfaces import IUserAchievementRepository
from app.application.entities import UserAchievement


class UserAchievementRepository(IUserAchievementRepository):
    """Реализация репозитория достижений пользователей"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user_achievement: UserAchievement) -> UserAchievement:
        self.session.add(user_achievement)
        return user_achievement
    
    async def get_by_user_id(self, user_id: int) -> list[UserAchievement]:
        result = await self.session.execute(
            select(UserAchievement).where(UserAchievement.user_id == user_id)
        )
        return list(result.scalars()) 