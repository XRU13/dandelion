from pydantic import BaseModel, Field
from datetime import datetime
from app.application.entities import EventType


class EventDetails(BaseModel):
	"""Детали события"""
	level_id: int | None = Field(None,
	                             description="ID уровня для complete_level")
	item_id: str | None = Field(None, description="ID предмета для find_secret")
	location: str | None = Field(None, description="Локация для find_secret")


class EventRequest(BaseModel):
	"""Модель запроса для создания события"""
	user_id: int = Field(..., description="ID пользователя", gt=0)
	event_type: EventType = Field(..., description="Тип события")
	details: EventDetails | None = Field(
		None,
		description="Дополнительные данные события")


class EventResponse(BaseModel):
	"""Модель ответа события"""
	id: int = Field(..., description="ID события")
	user_id: int = Field(..., description="ID пользователя")
	event_type: str = Field(..., description="Тип события")
	details: EventDetails | None = Field(None,
	                                     description="Дополнительные данные")
	created_at: datetime = Field(..., description="Время создания")
	message: str = Field(..., description="Сообщение о результате")

	model_config = {"from_attributes": True}
