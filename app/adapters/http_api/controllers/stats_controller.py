from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.stats_schemas import UserStatsResponse
from app.adapters.http_api.dependencies import get_stats_service

router = APIRouter(prefix="/stats", tags=["statistics"])

@router.get("/{user_id}", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: int,
    stats_service = Depends(get_stats_service)
):
    """
    Получить полную статистику пользователя.
    
    Endpoint: GET /stats/{user_id}
    Возвращает:
    - "score": общий счет пользователя из Redis (ключ: user:{user_id}:score)
    - "achievements": список названий достижений ["Новичок", "Исследователь"]
    - "last_events": последние 5 событий из БД
    """
    stats_data = await stats_service.get_user_stats(user_id)
    return UserStatsResponse(
        user_id=stats_data["user_id"],
        total_score=stats_data["total_score"],
        achievements_count=stats_data["achievements_count"],
        login_count=stats_data["login_count"],
        levels_completed=stats_data["levels_completed"],
        secrets_found=stats_data["secrets_found"],
        last_activity=stats_data["last_activity"]
    ) 