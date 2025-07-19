from datetime import datetime
from dataclasses import dataclass
from .enums import EventType


@dataclass  
class Event:
    """Сущность события пользователя"""
    user_id: int
    event_type: EventType
    id: int | None = None
    details: dict | None = None  # JSON с деталями события
    created_at: datetime | None = None 