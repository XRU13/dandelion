from fastapi import APIRouter, Depends

from app.adapters.http_api.schemas.achievement_schemas import (
    AchievementResponse,
    UserAchievementResponse,
)
from app.adapters.http_api.dependencies import get_achievement_service

router = APIRouter(
    prefix="/achievements",
    tags=["achievements"],
    responses={404: {"description": "Not Found"}},
)

@router.get(
    "/",
    response_model=list[AchievementResponse],
    summary="Получить все доступные достижения",
    response_description="Список всех доступных достижений"
)
async def get_all_achievements(
    achievement_service = Depends(get_achievement_service)
) -> list[AchievementResponse]:
    """Получить все доступные достижения"""
    achievements = await achievement_service.get_all_achievements()
    return [
        AchievementResponse(
            id=achievement.id,
            type=achievement.type,
            name=achievement.name,
            description=achievement.description,
            points=achievement.points,
            condition_field=achievement.condition_field,
            condition_value=achievement.condition_value,
            created_at=achievement.created_at
        )
        for achievement in achievements
    ]

@router.get(
    "/users/{user_id}",
    response_model=list[UserAchievementResponse],
    summary="Получить достижения пользователя",
    response_description="Список достижений пользователя"
)
async def get_user_achievements(
    user_id: int,
    achievement_service = Depends(get_achievement_service)
) -> list[UserAchievementResponse]:
    """Получить достижения конкретного пользователя"""
    achievements_data = await (
        achievement_service.get_user_achievements_with_details(
            user_id=user_id
        )
    )
    return [
        UserAchievementResponse(
            id=data["id"],
            user_id=data["user_id"],
            achievement_id=data["achievement_id"],
            achievement_name=data["achievement_name"],
            points=data["points"],
            earned_at=data["earned_at"]
        )
        for data in achievements_data
    ] 