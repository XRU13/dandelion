from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.user_schemas import (
    UserResponse,
    UserScoreResponse,
    UserCreateRequest,
)
from app.adapters.http_api.dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/",
    response_model=UserResponse,
    summary="Создать нового пользователя",
    response_description="Информация о созданном пользователе"
)
async def create_user(
    user_data: UserCreateRequest,
    user_service = Depends(get_user_service)
) -> UserResponse:
    """Создать нового пользователя"""
    user = await user_service.create_user(
        username=user_data.username,
        email=user_data.email
    )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Получить всех пользователей",
    response_description="Список всех пользователей"
)
async def get_all_users(
    user_service = Depends(get_user_service)
) -> list[UserResponse]:
    """Получить всех пользователей"""
    users = await user_service.get_all_users()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
        for user in users
    ]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя по ID",
    response_description="Информация о пользователе"
)
async def get_user(
    user_id: int,
    user_service = Depends(get_user_service)
) -> UserResponse:
    """Получить информацию о пользователе"""
    user = await user_service.get_user_by_id(user_id)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )

@router.get(
    "/{user_id}/score",
    response_model=UserScoreResponse,
    summary="Получить счет пользователя",
    response_description="Статистика активности пользователя"
)
async def get_user_score(
    user_id: int,
    user_service = Depends(get_user_service)
) -> UserScoreResponse:
    """Получить счет пользователя"""
    score = await user_service.get_user_score(user_id)
    return UserScoreResponse(
        user_id=score.user_id,
        login_count=score.login_count,
        levels_completed=score.levels_completed,
        secrets_found=score.secrets_found,
        updated_at=score.updated_at
    )
