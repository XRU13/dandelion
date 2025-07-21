from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



from app.application.interfaces import IAchievementRepository
from app.application.entities import Achievement


class AchievementRepository(IAchievementRepository):
    """Реализация репозитория достижений"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> list[Achievement]:
        result = await self.session.execute(select(Achievement))
        return list(result.scalars())
    
    async def get_by_id(self, achievement_id: int) -> Achievement | None:
        result = await self.session.execute(
            select(Achievement).where(Achievement.id == achievement_id)
        )
        return result.scalar_one_or_none() 