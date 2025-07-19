from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.application.interfaces import IUserAchievementRepository
from app.application.entities import UserAchievement


class UserAchievementRepository(IUserAchievementRepository):
    """Реализация репозитория достижений пользователей на SQLAlchemy"""
    
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
    
    async def exists(self, user_id: int, achievement_id: int) -> bool:
        result = await self.session.execute(
            select(UserAchievement).where(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id
            )
        )
        return result.scalar_one_or_none() is not None 