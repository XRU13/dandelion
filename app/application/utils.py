"""
Утилиты для работы с событиями, очками и достижениями
"""
from app.application.entities import EventType, UserScore
from app.application.constants import EventPoints


class ScoreCalculator:
    """Класс для расчета очков и проверки достижений"""
    
    @staticmethod
    def calculate_event_points(event_type: EventType) -> int:
        """Рассчитывает очки за событие согласно ТЗ"""
        points_mapping = {
            EventType.LOGIN: EventPoints.LOGIN,
            EventType.COMPLETE_LEVEL: EventPoints.COMPLETE_LEVEL,
            EventType.FIND_SECRET: EventPoints.FIND_SECRET,
        }
        return points_mapping.get(event_type, 0)
    
    @staticmethod
    def calculate_total_score(user_score: UserScore) -> int:
        """Рассчитывает общий счет пользователя"""
        return (
            user_score.login_count * EventPoints.LOGIN +
            user_score.levels_completed * EventPoints.COMPLETE_LEVEL +
            user_score.secrets_found * EventPoints.FIND_SECRET
        )
    
    @staticmethod
    def update_user_score_counters(user_score: UserScore, event_type: EventType) -> None:
        """Обновляет счетчики пользователя в зависимости от типа события"""
        if event_type == EventType.LOGIN:
            user_score.login_count += 1
        elif event_type == EventType.COMPLETE_LEVEL:
            user_score.levels_completed += 1
        elif event_type == EventType.FIND_SECRET:
            user_score.secrets_found += 1


class AchievementChecker:
    """Класс для проверки условий достижений"""
    
    @staticmethod
    def check_achievement_condition(achievement, user_score: UserScore) -> bool:
        """Проверяет выполнение условия достижения"""
        field_value = getattr(user_score, achievement.condition_field, 0)
        return field_value >= achievement.condition_value
    
    @staticmethod
    def get_earned_achievement_ids(user_achievements) -> set[int]:
        """Возвращает множество ID уже полученных достижений"""
        return {ua.achievement_id for ua in user_achievements}


class ValidationHelper:
    """Класс для валидации данных"""
    
    @staticmethod
    def validate_user_id(user_id: int) -> bool:
        """Проверяет корректность ID пользователя"""
        return isinstance(user_id, int) and user_id > 0
    
    @staticmethod
    def validate_event_details(details: dict | None) -> bool:
        """Проверяет корректность деталей события"""
        if details is None:
            return True
        
        if not isinstance(details, dict):
            return False
        
        # Проверяем размер JSON
        import json
        try:
            json_str = json.dumps(details)
            return len(json_str.encode('utf-8')) <= 1024  # Лимит из констант
        except (TypeError, ValueError):
            return False 