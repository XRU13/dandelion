from datetime import datetime
from dataclasses import dataclass


@dataclass
class AchievementNotification:
    """Сущность уведомления о достижении"""
    user_id: int
    achievement_id: int
    message: str
    is_sent: bool = False
    id: int | None = None
    created_at: datetime | None = None
    sent_at: datetime | None = None 