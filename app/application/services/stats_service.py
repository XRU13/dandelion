from app.application.interfaces import (
    IUserRepository, IUserScoreRepository, IUserAchievementRepository
)
from app.application.exceptions import UserNotFoundError, StatsServiceError
from app.application.utils import ScoreCalculator


class StatsService:
    """Сервис для работы со статистикой пользователей"""
    
    def __init__(
        self,
        user_repo: IUserRepository,
        user_score_repo: IUserScoreRepository,
        user_achievement_repo: IUserAchievementRepository,
        redis_cache=None
    ):
        self.user_repo = user_repo
        self.user_score_repo = user_score_repo
        self.user_achievement_repo = user_achievement_repo
        self.redis_cache = redis_cache
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Получить полную статистику пользователя"""
        try:
            # Проверяем существование пользователя
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            
            # Получаем счет пользователя
            user_score = await self.user_score_repo.get_by_user_id(user_id)
            if not user_score:
                # Если счета нет, создаем базовую статистику
                return {
                    "user_id": user_id,
                    "total_score": 0,
                    "achievements_count": 0,
                    "login_count": 0,
                    "levels_completed": 0,
                    "secrets_found": 0,
                    "last_activity": None
                }
            
            # Получаем количество достижений
            user_achievements = await self.user_achievement_repo.get_by_user_id(user_id)
            achievements_count = len(user_achievements)
            
            # Рассчитываем общий счет с помощью ScoreCalculator
            total_score = ScoreCalculator.calculate_total_score(user_score)
            
            # Пытаемся получить данные из Redis кэша
            cached_score = None
            if self.redis_cache:
                try:
                    cached_score = await self.redis_cache.get_score(user_id)
                except Exception:
                    pass  # Игнорируем ошибки Redis
            
            # Используем кэшированный счет, если он больше рассчитанного
            if cached_score and cached_score > total_score:
                total_score = cached_score
            
            return {
                "user_id": user_id,
                "total_score": total_score,
                "achievements_count": achievements_count,
                "login_count": user_score.login_count,
                "levels_completed": user_score.levels_completed,
                "secrets_found": user_score.secrets_found,
                "last_activity": user_score.updated_at
            }
            
        except Exception as e:
            if isinstance(e, UserNotFoundError):
                raise
            raise StatsServiceError(error=str(e)) 