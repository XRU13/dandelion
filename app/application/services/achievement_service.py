from datetime import datetime

from app.application.entities import Achievement, UserAchievement, AchievementNotification, UserScore
from app.application.interfaces import (
    IAchievementRepository, IUserAchievementRepository, 
    IAchievementNotificationRepository, IUserScoreRepository
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
    
    async def check_achievements(self, user_id: int) -> list[Achievement]:
        """Проверяет и присваивает новые достижения пользователю"""
        try:
            # Получаем статистику пользователя
            user_score = await self.user_score_repo.get_by_user_id(user_id)
            if not user_score:
                return []  # Нет статистики = нет достижений
            
            # Получаем все доступные достижения
            all_achievements = await self.achievement_repo.get_all()
            
            # Получаем уже полученные достижения пользователя
            user_achievements = await self.user_achievement_repo.get_by_user_id(user_id)
            earned_achievement_ids = {ua.achievement_id for ua in user_achievements}
            
            new_achievements = []
            
            # Проверяем каждое достижение
            for achievement in all_achievements:
                if achievement.id in earned_achievement_ids:
                    continue  # Уже получено
                
                # Проверяем условия достижения
                if self._check_achievement_condition(achievement, user_score):
                    # Присваиваем достижение
                    user_achievement = UserAchievement(
                        user_id=user_id,
                        achievement_id=achievement.id
                    )
                    await self.user_achievement_repo.create(user_achievement)
                    
                    # Создаем уведомление
                    notification = AchievementNotification(
                        user_id=user_id,
                        achievement_id=achievement.id,
                        message=f"Поздравляем! Вы получили достижение: {achievement.name}"
                    )
                    await self.notification_repo.create(notification)
                    
                    new_achievements.append(achievement)
            
            return new_achievements
            
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при проверке достижений: {e}")
    
    def _check_achievement_condition(self, achievement: Achievement, user_score: UserScore) -> bool:
        """Проверяет выполнение условия достижения"""
        if achievement.condition_field == "login_count":
            return user_score.login_count >= achievement.condition_value
        elif achievement.condition_field == "levels_completed":
            return user_score.levels_completed >= achievement.condition_value
        elif achievement.condition_field == "secrets_found":
            return user_score.secrets_found >= achievement.condition_value
        
        return False
    
    async def get_all_achievements(self) -> list[Achievement]:
        """Получить все доступные достижения"""
        try:
            return await self.achievement_repo.get_all()
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при получении достижений: {e}")
    
    async def get_user_achievements(self, user_id: int) -> list[UserAchievement]:
        """Получить все достижения пользователя"""
        try:
            return await self.user_achievement_repo.get_by_user_id(user_id)
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при получении достижений пользователя: {e}")
    
    async def get_user_achievements_with_details(self, user_id: int) -> list[dict]:
        """Получить достижения пользователя с подробностями"""
        try:
            user_achievements = await self.user_achievement_repo.get_by_user_id(user_id)
            detailed_achievements = []
            
            for user_achievement in user_achievements:
                achievement = await self.achievement_repo.get_by_id(user_achievement.achievement_id)
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
            raise AchievementServiceError(f"Ошибка при получении детальных достижений: {e}")
    
    async def create_notification(self, user_id: int, achievement_id: int, message: str) -> AchievementNotification:
        """Создать уведомление о достижении"""
        try:
            notification = AchievementNotification(
                user_id=user_id,
                achievement_id=achievement_id,
                message=message
            )
            return await self.notification_repo.create(notification)
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при создании уведомления: {e}")
    
    async def get_unsent_notifications(self) -> list[AchievementNotification]:
        """Получить неотправленные уведомления"""
        try:
            return await self.notification_repo.get_unsent()
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при получении уведомлений: {e}")
    
    async def mark_notification_as_sent(self, notification_id: int) -> None:
        """Отметить уведомление как отправленное"""
        try:
            await self.notification_repo.mark_as_sent(notification_id)
        except Exception as e:
            raise AchievementServiceError(f"Ошибка при обновлении уведомления: {e}") 