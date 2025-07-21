from pydantic import BaseModel, Field
from datetime import datetime
from app.application.constants import Limits


class AchievementResponse(BaseModel):
	"""Модель ответа достижения"""
	id: int = Field(..., description="ID достижения")
	type: str = Field(..., description="Тип достижения",
	                  max_length=Limits.ACHIEVEMENT_TYPE_MAX_LENGTH)
	name: str = Field(..., description="Название достижения",
	                  max_length=Limits.ACHIEVEMENT_NAME_MAX_LENGTH)
	description: str = Field(..., description="Описание достижения")
	points: int = Field(..., description="Очки за достижение", ge=0)
	condition_field: str = Field(..., description="Поле для проверки",
	                             max_length=Limits.ACHIEVEMENT_TYPE_MAX_LENGTH)
	condition_value: int = Field(..., description="Значение для достижения",
	                             ge=0)
	created_at: datetime = Field(..., description="Дата создания")

	model_config = {"from_attributes": True}


class UserAchievementResponse(BaseModel):
	"""Модель ответа достижения пользователя"""
	id: int = Field(..., description="ID записи")
	user_id: int = Field(..., description="ID пользователя")
	achievement_id: int = Field(..., description="ID достижения")
	achievement_name: str = Field(..., description="Название достижения",
	                              max_length=Limits.ACHIEVEMENT_NAME_MAX_LENGTH)
	points: int = Field(..., description="Очки за достижение", ge=0)
	earned_at: datetime = Field(..., description="Время получения")

	model_config = {"from_attributes": True}
