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


# Исключения для пользователей
class UserNotFoundError(AppError):
    """Исключение для случая когда пользователь не найден"""
    msg_template = 'Пользователь с ID {user_id} не найден'
    code = 'user_service.user_not_found'


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


# Исключения для достижений
class AchievementServiceError(AppError):
    """Базовое исключение для сервиса достижений"""
    msg_template = 'Ошибка сервиса достижений: {error}'
    code = 'achievement_service.error'


# Исключения для статистики
class StatsServiceError(AppError):
    """Базовое исключение для сервиса статистики"""
    msg_template = 'Ошибка сервиса статистики: {error}'
    code = 'stats_service.error'


# Исключения для валидации
class ValidationError(AppError):
    """Базовое исключение для ошибок валидации"""
    msg_template = 'Ошибка валидации: {field} - {error}'
    code = 'validation.error'
