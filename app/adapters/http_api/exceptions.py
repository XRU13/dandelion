from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.application.services.user_service import UserNotFoundError, UserScoreNotFoundError
from app.application.services.stats_service import UserNotFoundError as StatsUserNotFoundError
from app.application.services.achievement_service import AchievementServiceError
from app.application.services.event_service import (
    UserNotFoundError as EventUserNotFoundError,
    InvalidEventDataError,
    EventServiceError
)


class ExceptionHandler:
    """Централизованный обработчик исключений"""
    
    @staticmethod
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def user_score_not_found_handler(request: Request, exc: UserScoreNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def stats_user_not_found_handler(request: Request, exc: StatsUserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def event_user_not_found_handler(request: Request, exc: EventUserNotFoundError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def invalid_event_data_handler(request: Request, exc: InvalidEventDataError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def achievement_service_error_handler(request: Request, exc: AchievementServiceError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def event_service_error_handler(request: Request, exc: EventServiceError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )
    
    @staticmethod
    async def runtime_error_handler(request: Request, exc: RuntimeError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        ) 