from abc import ABC, abstractmethod
from app.application.entities import User


class IUserRepository(ABC):
	"""Абстрактный репозиторий пользователей"""

	@abstractmethod
	async def create(self, user: User) -> User:
		pass

	@abstractmethod
	async def get_all(self) -> list[User]:
		pass

	@abstractmethod
	async def get_by_id(self, user_id: int) -> User | None:
		pass
