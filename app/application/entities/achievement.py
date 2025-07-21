from datetime import datetime
from dataclasses import dataclass
from .enums import AchievementType


@dataclass
class Achievement:
    """Сущность определения достижения"""
    type: AchievementType
    name: str
    description: str
    points: int  # Количество очков за достижение
    condition_field: str  # Поле для проверки (login_count, levels_completed)
    condition_value: int  # Значение для достижения
    id: int | None = None
    created_at: datetime | None = None 