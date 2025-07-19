from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



from app.application.interfaces import IUserRepository
from app.application.entities import User


class UserRepository(IUserRepository):
    """Реализация репозитория пользователей на SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        return user
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none() 