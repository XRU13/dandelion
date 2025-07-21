from pydantic import BaseModel, Field
from datetime import datetime
from app.application.constants import Limits


class LastEventResponse(BaseModel):
	"""Модель последнего события"""
	id: int = Field(..., description="ID события")
	event_type: str = Field(..., description="Тип события")
	details: dict | None = Field(None, description="Детали события")
	created_at: datetime = Field(..., description="Время создания")


class UserStatsResponse(BaseModel):
	"""Модель ответа статистики пользователя согласно ТЗ"""
	user_id: int = Field(..., description="ID пользователя")
	score: int = Field(..., description="Общий счет из Redis", ge=0)
	achievements: list[str] = Field(...,
	                                description="Список названий достижений")
	last_events: list[LastEventResponse] = Field(
		...,
		description=f"Последние {Limits.RECENT_EVENTS_LIMIT} событий из БД")

	model_config = {"from_attributes": True}
