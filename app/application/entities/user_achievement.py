from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserAchievement:
    """Сущность полученного достижения"""
    user_id: int
    achievement_id: int
    id: int | None = None
    earned_at: datetime | None = None 