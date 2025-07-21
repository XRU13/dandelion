from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.application.interfaces import IUserScoreRepository
from app.application.entities import UserScore


class UserScoreRepository(IUserScoreRepository):
    """Реализация репозитория счетов пользователей """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_user_id(self, user_id: int) -> UserScore | None:
        result = await self.session.execute(
            select(UserScore).where(UserScore.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user_score: UserScore) -> UserScore:
        user_score.updated_at = datetime.now(timezone.utc)
        self.session.add(user_score)
        return user_score
    
    async def create(self, user_score: UserScore) -> UserScore:
        if user_score.updated_at is None:
            user_score.updated_at = datetime.now(timezone.utc)
        self.session.add(user_score)
        return user_score 