from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.user_schemas import UserResponse, UserScoreResponse
from app.adapters.http_api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service = Depends(get_user_service)
):
    """Получить информацию о пользователе"""
    user = await user_service.get_user_by_id(user_id)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )

@router.get("/{user_id}/score", response_model=UserScoreResponse)
async def get_user_score(
    user_id: int,
    user_service = Depends(get_user_service)
):
    """Получить счет пользователя"""
    score = await user_service.get_user_score(user_id)
    return UserScoreResponse(
        user_id=score.user_id,
        login_count=score.login_count,
        levels_completed=score.levels_completed,
        secrets_found=score.secrets_found,
        updated_at=score.updated_at
    ) 