from enum import Enum


class EventType(str, Enum):
    """Типы событий"""
    LOGIN = "login"
    COMPLETE_LEVEL = "complete_level" 
    FIND_SECRET = "find_secret"


class AchievementType(str, Enum):
    """Типы достижений"""
    NEWCOMER = "newcomer"  # 1+ вход
    RESEARCHER = "researcher"  # 3+ найденных секрета
    MASTER = "master"  # 10+ завершенных уровней 