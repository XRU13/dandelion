from pydantic import BaseModel, Field
from datetime import datetime

class UserStatsResponse(BaseModel):
    """Модель ответа статистики пользователя"""
    user_id: int = Field(..., description="ID пользователя")
    total_score: int = Field(..., description="Общий счет", ge=0)
    achievements_count: int = Field(..., description="Количество достижений", ge=0)
    login_count: int = Field(..., description="Количество входов", ge=0)
    levels_completed: int = Field(..., description="Завершенные уровни", ge=0)
    secrets_found: int = Field(..., description="Найденные секреты", ge=0)
    last_activity: datetime = Field(..., description="Последняя активность")
    
    model_config = {"from_attributes": True} 