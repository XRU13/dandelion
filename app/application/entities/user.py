from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """Сущность пользователя"""
    username: str
    email: str
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None 