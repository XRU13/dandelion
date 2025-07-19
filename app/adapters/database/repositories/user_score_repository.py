from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



from app.application.interfaces import IUserScoreRepository
from app.application.entities import UserScore


class UserScoreRepository(IUserScoreRepository):
    """Реализация репозитория счетов пользователей на SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_user_id(self, user_id: int) -> UserScore | None:
        result = await self.session.execute(
            select(UserScore).where(UserScore.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user_score: UserScore) -> UserScore:
        return user_score
    
    async def create(self, user_score: UserScore) -> UserScore:
        self.session.add(user_score)
        return user_score 