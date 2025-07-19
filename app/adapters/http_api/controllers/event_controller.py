from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.event_schemas import EventRequest, EventResponse, EventDetails
from app.adapters.http_api.dependencies import get_event_service

router = APIRouter(prefix="/event", tags=["events"])

@router.post("/", response_model=EventResponse)
async def create_event(
    event_request: EventRequest,
    event_service = Depends(get_event_service)
):
    """
    Создает новое событие пользователя согласно ТЗ.
    
    Поддерживаемые типы событий:
    - login: Вход пользователя в игру (5 очков)
    - complete_level: Завершение уровня (20 очков)
    - find_secret: Найден секретный объект (50 очков)
    
    Примеры деталей события:
    - Для login: null (пустые детали)
    - Для complete_level: {"level_id": 5}
    - Для find_secret: {"item_id": "chest_01", "location": "forest_cave"}
    """
    event = await event_service.process_event(
        user_id=event_request.user_id,
        event_type=event_request.event_type,
        details=event_request.details.model_dump() if event_request.details else None
    )
    
    return EventResponse(
        id=event.id,
        user_id=event.user_id,
        event_type=event.event_type if isinstance(event.event_type, str) else event.event_type.value,
        details=EventDetails(**event.details) if event.details else None,
        created_at=event.created_at,
        message="Событие создано и отправлено на обработку"
    ) 