from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.stats_schemas import (
    UserStatsResponse,
    LastEventResponse,
)
from app.adapters.http_api.dependencies import get_stats_service

router = APIRouter(
    prefix="/stats",
    tags=["statistics"],
    responses={404: {"description": "Not Found"}},
)

@router.get(
    "/{user_id}",
    response_model=UserStatsResponse,
    summary="Получить статистику пользователя",
    response_description="Полная статистика пользователя"
)
async def get_user_stats(
    user_id: int,
    stats_service = Depends(get_stats_service)
) -> UserStatsResponse:
    """
    Получить полную статистику пользователя.
    
    Возвращает:
    - "score": общий счет пользователя из Redis (ключ: user:{user_id}:score)
    - "achievements": список названий достижений ["Новичок", "Исследователь"]
    - "last_events": последние {Limits.RECENT_EVENTS_LIMIT} событий из БД
    """
    stats_data = await stats_service.get_user_stats(user_id)
    return UserStatsResponse(
        user_id=stats_data["user_id"],
        score=stats_data["score"],
        achievements=stats_data["achievements"],
        last_events=[
            LastEventResponse(**event_data) 
            for event_data in stats_data["last_events"]
        ]
    ) 