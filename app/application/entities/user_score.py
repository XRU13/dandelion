from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserScore:
    """Сущность счета пользователя"""
    user_id: int
    login_count: int = 0
    levels_completed: int = 0
    secrets_found: int = 0
    id: int | None = None
    updated_at: datetime | None = None 