from abc import ABC, abstractmethod


from ..entities import User


class IUserRepository(ABC):
    """Абстрактный репозиторий пользователей"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass