from fastapi import APIRouter, Depends
from app.adapters.http_api.schemas.event_schemas import (
	EventRequest,
	EventResponse,
	EventDetails,
)
from app.adapters.http_api.dependencies import get_event_service
from app.application.utils import EventTypeHelper

router = APIRouter(
    prefix="/event",
    tags=["events"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/",
    response_model=EventResponse,
    summary="Создать событие пользователя",
    response_description="Информация о созданном событии"
)
async def create_event(
	event_request: EventRequest,
	event_service=Depends(get_event_service)
) -> EventResponse:
	"""
	Создает новое событие пользователя.

	Поддерживаемые типы событий:
	- login: Вход пользователя в игру
	- complete_level: Завершение уровня
	- find_secret: Найден секретный объект
	"""
	event = await event_service.process_event(
		user_id=event_request.user_id,
		event_type=event_request.event_type,
		details=event_request.details.model_dump() if event_request.details else None
	)

	return EventResponse(
		id=event.id,
		user_id=event.user_id,
		event_type=EventTypeHelper.to_string(event.event_type),
		details=EventDetails(**event.details) if event.details else None,
		created_at=event.created_at,
		message="Событие создано и отправлено на обработку"
	)
