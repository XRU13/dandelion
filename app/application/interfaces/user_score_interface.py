from abc import ABC, abstractmethod

from app.application.entities import UserScore


class IUserScoreRepository(ABC):
	"""Абстрактный репозиторий счетов пользователей"""

	@abstractmethod
	async def get_by_user_id(self, user_id: int) -> UserScore | None:
		pass

	@abstractmethod
	async def update(self, user_score: UserScore) -> UserScore:
		pass

	@abstractmethod
	async def create(self, user_score: UserScore) -> UserScore:
		pass
