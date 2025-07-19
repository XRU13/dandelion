from pydantic import BaseModel, Field
from datetime import datetime

class UserResponse(BaseModel):
    """Модель ответа пользователя"""
    id: int = Field(..., description="ID пользователя")
    username: str = Field(..., description="Имя пользователя", max_length=50)
    email: str = Field(..., description="Email пользователя", max_length=100)
    created_at: datetime = Field(..., description="Дата создания")
    
    model_config = {"from_attributes": True}

class UserScoreResponse(BaseModel):
    """Модель ответа счета пользователя"""
    user_id: int = Field(..., description="ID пользователя")
    login_count: int = Field(..., description="Количество входов", ge=0)
    levels_completed: int = Field(..., description="Завершенные уровни", ge=0)
    secrets_found: int = Field(..., description="Найденные секреты", ge=0)
    updated_at: datetime = Field(..., description="Время последнего обновления")
    
    model_config = {"from_attributes": True} 