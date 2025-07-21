"""
Константы приложения для системы событий и достижений
"""

# Очки за события согласно ТЗ
class EventPoints:
    """Константы очков за различные события"""
    LOGIN = 5
    COMPLETE_LEVEL = 20
    FIND_SECRET = 50


class CacheSettings:
    """Настройки Redis кэша"""
    DEFAULT_TTL = 3600  # 1 час

    SCORE_KEY_PREFIX = "user:"
    SCORE_KEY_SUFFIX = ":score"

    EVENT_KEY_PREFIX = "user_events:"
    ACHIEVEMENT_KEY_PREFIX = "user_achievements:"

    STATS_KEY_PREFIX = "user:"
    STATS_KEY_SUFFIX = ":stats"
    STATS_TTL = 60  # 1 минута

    @staticmethod
    def get_score_key(user_id: int) -> str:
        return f"{CacheSettings.SCORE_KEY_PREFIX}{user_id}{CacheSettings.SCORE_KEY_SUFFIX}"

    @staticmethod
    def get_events_key(user_id: int) -> str:
        return f"{CacheSettings.EVENT_KEY_PREFIX}{user_id}"

    @staticmethod
    def get_achievements_key(user_id: int) -> str:
        return f"{CacheSettings.ACHIEVEMENT_KEY_PREFIX}{user_id}"

    @staticmethod
    def get_stats_key(user_id: int) -> str:
        return f"{CacheSettings.STATS_KEY_PREFIX}{user_id}{CacheSettings.STATS_KEY_SUFFIX}"


# Лимиты системы
class Limits:
    """Лимиты и ограничения системы"""
    EVENTS_IN_CACHE = 10  # Количество событий в Redis кеше
    RECENT_EVENTS_LIMIT = 5  # Лимит последних событий по умолчанию
    MAX_JSON_SIZE_BYTES = 1024  # Максимальный размер JSON в байтах
    USERNAME_MAX_LENGTH = 50  # Максимальная длина имени пользователя
    EMAIL_MAX_LENGTH = 100  # Максимальная длина email
    ACHIEVEMENT_TYPE_MAX_LENGTH = 50  # Максимальная длина типа достижения
    ACHIEVEMENT_NAME_MAX_LENGTH = 100  # Максимальная длина названия достижения
    EVENT_TYPE_MAX_LENGTH = 50  # Максимальная длина типа события


# Поля базы данных
class DatabaseFields:
    """Названия полей в базе данных"""
    LOGIN_COUNT = "login_count"
    LEVELS_COMPLETED = "levels_completed"
    SECRETS_FOUND = "secrets_found"
    LEVEL_ID = "level_id"


# Конфигурация Redis
class RedisConfig:
    """Настройки Redis"""
    DEFAULT_URL = "redis://localhost:6379/0"


# Конфигурация Celery
class CeleryConfig:
    """Настройки Celery"""
    RESULT_EXPIRES = 3600  # Время жизни результата в секундах


# Сообщения
class Messages:
    """Константы сообщений"""
    EVENT_PROCESSING_SUCCESS = "Event {event_id} processed: +{points} points (total: {total_score})"
    EVENT_PROCESSING_ERROR = "Error processing event {event_id}: {error}"