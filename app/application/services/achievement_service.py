from app.application.entities import Achievement
from app.application.interfaces import (
	IAchievementRepository,
	IUserAchievementRepository,
	IAchievementNotificationRepository,
	IUserScoreRepository,
)
from app.application.exceptions import AchievementServiceError


class AchievementService:
	"""Сервис для обработки системы достижений"""

	def __init__(
		self,
		achievement_repo: IAchievementRepository,
		user_achievement_repo: IUserAchievementRepository,
		notification_repo: IAchievementNotificationRepository,
		user_score_repo: IUserScoreRepository,
		redis_cache=None
	):
		self.achievement_repo = achievement_repo
		self.user_achievement_repo = user_achievement_repo
		self.notification_repo = notification_repo
		self.user_score_repo = user_score_repo
		self.redis_cache = redis_cache

	async def get_all_achievements(self) -> list[Achievement]:
		"""Получить все доступные достижения"""
		try:
			return await self.achievement_repo.get_all()
		except Exception as e:
			raise AchievementServiceError(error=str(e))

	async def get_user_achievements_with_details(
		self,
		user_id: int,
	) -> list[dict]:
		"""Получить достижения пользователя с подробностями"""
		try:
			user_achievements = await self.user_achievement_repo.get_by_user_id(
				user_id=user_id
			)
			detailed_achievements = []

			for user_achievement in user_achievements:
				achievement = await self.achievement_repo.get_by_id(
					user_achievement.achievement_id)
				if achievement:
					detailed_achievements.append({
						"id": user_achievement.id,
						"user_id": user_achievement.user_id,
						"achievement_id": user_achievement.achievement_id,
						"achievement_name": achievement.name,
						"points": achievement.points,
						"earned_at": user_achievement.earned_at
					})

			return detailed_achievements

		except Exception as e:
			raise AchievementServiceError(error=str(e))
