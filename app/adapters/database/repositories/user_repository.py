from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



from app.application.interfaces import IUserRepository
from app.application.entities import User


class UserRepository(IUserRepository):
    """Реализация репозитория пользователей"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars())
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    