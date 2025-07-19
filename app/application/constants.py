"""
Константы приложения для системы событий и достижений
"""

# Очки за события согласно ТЗ
class EventPoints:
    """Константы очков за различные события"""
    LOGIN = 5
    COMPLETE_LEVEL = 20
    FIND_SECRET = 50


# Настройки кэша
class CacheSettings:
    """Настройки Redis кэша"""
    DEFAULT_TTL = 3600  # 1 час
    SCORE_KEY_PREFIX = "user_score:"
    EVENT_KEY_PREFIX = "user_events:"
    ACHIEVEMENT_KEY_PREFIX = "user_achievements:"


# Настройки базы данных
class DatabaseSettings:
    """Настройки базы данных"""
    QUERY_TIMEOUT = 30  # секунд
    CONNECTION_POOL_SIZE = 10
    MAX_OVERFLOW = 20


# Настройки Celery
class CelerySettings:
    """Настройки Celery задач"""
    TASK_TIMEOUT = 300  # 5 минут
    RETRY_DELAY = 60    # 1 минута
    MAX_RETRIES = 3


# Лимиты и ограничения
class Limits:
    """Лимиты системы"""
    MAX_EVENTS_PER_USER_PER_DAY = 1000
    MAX_ACHIEVEMENTS_PER_USER = 100
    MAX_DETAILS_JSON_SIZE = 1024  # байт


# Сообщения
class Messages:
    """Константы сообщений"""
    EVENT_CREATED = "Событие создано и отправлено на обработку"
    ACHIEVEMENT_EARNED = "Поздравляем! Вы получили достижение: {name}"
    REDIS_CACHE_ERROR = "Failed to update Redis cache for user {user_id}: {error}"
    EVENT_PROCESSING_SUCCESS = "Event {event_id} processed: +{points} points (total: {total_score})"
    EVENT_PROCESSING_ERROR = "Error processing event {event_id}: {error}"
    USER_NOT_FOUND = "Пользователь с ID {user_id} не найден"
    EVENT_NOT_FOUND = "Событие с ID {event_id} не найдено"


# Типы достижений и их условия
class AchievementConditions:
    """Условия для получения достижений"""
    
    # Достижения за входы
    NEWCOMER_LOGINS = 1      # Новичок
    REGULAR_PLAYER_LOGINS = 10   # Постоянный игрок  
    VETERAN_LOGINS = 50      # Ветеран
    
    # Достижения за уровни
    BEGINNER_LEVELS = 1      # Начинающий
    ACHIEVER_LEVELS = 5      # Достигатор
    MASTER_LEVELS = 20       # Мастер
    CHAMPION_LEVELS = 50     # Чемпион
    
    # Достижения за секреты
    EXPLORER_SECRETS = 1     # Исследователь
    TREASURE_HUNTER_SECRETS = 5  # Охотник за сокровищами
    SECRET_MASTER_SECRETS = 15   # Мастер секретов


# Настройки логирования
class LoggingSettings:
    """Настройки логирования"""
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    FILE_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5 