"""
Модуль с пользовательскими исключениями для приложения
"""


class AppError(Exception):
    """
    Базовый класс для ошибок приложения.
    """
    msg_template: str = None
    code: str

    def __init__(self, **kwargs):
        self.context = kwargs.pop('context', {})

        if 'message' in kwargs:
            self.message = kwargs['message']
        elif self.msg_template:
            self.message = self.msg_template.format(**kwargs)
        else:
            self.message = None

    def __str__(self):
        return self.message


# Базовые исключения
class ApplicationError(AppError):
    """Базовое исключение для приложения"""
    code = 'application.error'


# Исключения для пользователей
class UserNotFoundError(AppError):
    """Исключение для случая когда пользователь не найден"""
    msg_template = 'Пользователь с ID {user_id} не найден'
    code = 'user_service.user_not_found'


class UserAlreadyExistsError(AppError):
    """Исключение для случая когда пользователь уже существует"""
    msg_template = 'Пользователь {username} уже существует'
    code = 'user_service.user_already_exists'


class UserScoreNotFoundError(AppError):
    """Исключение для случая когда счет пользователя не найден"""
    msg_template = 'Счет для пользователя {user_id} не найден'
    code = 'user_service.user_score_not_found'


# Исключения для событий
class EventNotFoundError(AppError):
    """Исключение для случая когда событие не найдено"""
    msg_template = 'Событие с ID {event_id} не найдено'
    code = 'event_service.event_not_found'


class InvalidEventDataError(AppError):
    """Исключение для некорректных данных события"""
    msg_template = 'Некорректные данные события: {details}'
    code = 'event_service.invalid_event_data'


class EventServiceError(AppError):
    """Базовое исключение для сервиса событий"""
    msg_template = 'Ошибка сервиса событий: {error}'
    code = 'event_service.error'


class EventProcessingError(AppError):
    """Исключение для ошибок обработки событий"""
    msg_template = 'Ошибка при обработке события {event_id}: {error}'
    code = 'event_service.processing_error'


# Исключения для достижений
class AchievementNotFoundError(AppError):
    """Исключение для случая когда достижение не найдено"""
    msg_template = 'Достижение с ID {achievement_id} не найдено'
    code = 'achievement_service.achievement_not_found'


class AchievementServiceError(AppError):
    """Базовое исключение для сервиса достижений"""
    msg_template = 'Ошибка сервиса достижений: {error}'
    code = 'achievement_service.error'


class UserAchievementAlreadyExistsError(AppError):
    """Исключение для случая когда достижение уже выдано пользователю"""
    msg_template = 'Достижение {achievement_id} уже получено пользователем {user_id}'
    code = 'achievement_service.user_achievement_already_exists'


class AchievementConditionNotMetError(AppError):
    """Исключение для случая когда условие достижения не выполнено"""
    msg_template = 'Условие достижения {achievement_id} не выполнено для пользователя {user_id}'
    code = 'achievement_service.condition_not_met'


# Исключения для статистики
class StatsServiceError(AppError):
    """Базовое исключение для сервиса статистики"""
    msg_template = 'Ошибка сервиса статистики: {error}'
    code = 'stats_service.error'


class StatsNotFoundError(AppError):
    """Исключение для случая когда статистика не найдена"""
    msg_template = 'Статистика для пользователя {user_id} не найдена'
    code = 'stats_service.stats_not_found'


# Исключения для кэша
class CacheError(AppError):
    """Базовое исключение для операций с кэшем"""
    msg_template = 'Ошибка кэша: {error}'
    code = 'cache.error'


class CacheUnavailableError(CacheError):
    """Исключение для случая когда кэш недоступен"""
    msg_template = 'Кэш недоступен: {error}'
    code = 'cache.unavailable'


class CacheTimeoutError(CacheError):
    """Исключение для таймаута кэша"""
    msg_template = 'Таймаут операции с кэшем: {operation}'
    code = 'cache.timeout'


# Исключения для репозиториев
class RepositoryError(AppError):
    """Базовое исключение для репозиториев"""
    msg_template = 'Ошибка репозитория: {error}'
    code = 'repository.error'


class DatabaseConnectionError(RepositoryError):
    """Исключение для проблем с подключением к БД"""
    msg_template = 'Ошибка подключения к базе данных: {error}'
    code = 'repository.connection_error'


class DatabaseTimeoutError(RepositoryError):
    """Исключение для таймаутов БД"""
    msg_template = 'Таймаут операции с базой данных: {operation}'
    code = 'repository.timeout_error'


class DataIntegrityError(RepositoryError):
    """Исключение для нарушения целостности данных"""
    msg_template = 'Нарушение целостности данных: {details}'
    code = 'repository.data_integrity_error'


# Исключения для валидации
class ValidationError(AppError):
    """Базовое исключение для ошибок валидации"""
    msg_template = 'Ошибка валидации: {field} - {error}'
    code = 'validation.error'


class RequiredFieldError(ValidationError):
    """Исключение для отсутствующих обязательных полей"""
    msg_template = 'Обязательное поле {field} не заполнено'
    code = 'validation.required_field'


class InvalidFormatError(ValidationError):
    """Исключение для некорректного формата данных"""
    msg_template = 'Некорректный формат поля {field}: ожидается {expected}, получено {actual}'
    code = 'validation.invalid_format'


# Исключения для бизнес-логики
class BusinessLogicError(AppError):
    """Базовое исключение для нарушений бизнес-логики"""
    msg_template = 'Нарушение бизнес-логики: {rule}'
    code = 'business_logic.error'


class RateLimitExceededError(BusinessLogicError):
    """Исключение для превышения лимитов"""
    msg_template = 'Превышен лимит {limit_type} для пользователя {user_id}: {current}/{max}'
    code = 'business_logic.rate_limit_exceeded'


class InsufficientPermissionsError(BusinessLogicError):
    """Исключение для недостаточных прав"""
    msg_template = 'Недостаточно прав для выполнения операции {operation}'
    code = 'business_logic.insufficient_permissions' 