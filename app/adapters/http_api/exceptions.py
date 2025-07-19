from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.application.exceptions import (
    UserNotFoundError, UserScoreNotFoundError, EventNotFoundError,
    InvalidEventDataError, EventServiceError, AchievementServiceError,
    StatsServiceError, ValidationError, BusinessLogicError,
    CacheUnavailableError, RepositoryError
)


class ExceptionHandler:
    """Централизованный обработчик исключений"""
    
    @staticmethod
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def user_score_not_found_handler(request: Request, exc: UserScoreNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def event_not_found_handler(request: Request, exc: EventNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def invalid_event_data_handler(request: Request, exc: InvalidEventDataError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def business_logic_error_handler(request: Request, exc: BusinessLogicError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def event_service_error_handler(request: Request, exc: EventServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def achievement_service_error_handler(request: Request, exc: AchievementServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def stats_service_error_handler(request: Request, exc: StatsServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def cache_unavailable_handler(request: Request, exc: CacheUnavailableError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {}),
                "retry_after": 30  # Попробовать через 30 секунд
            }
        )
    
    @staticmethod
    async def repository_error_handler(request: Request, exc: RepositoryError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": str(exc),
                "error_code": exc.code,
                "context": getattr(exc, 'context', {})
            }
        )
    
    @staticmethod
    async def runtime_error_handler(request: Request, exc: RuntimeError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Внутренняя ошибка сервера",
                "error_code": "runtime.error",
                "context": {"original_error": str(exc)}
            }
        )
    
    @staticmethod
    async def generic_exception_handler(request: Request, exc: Exception):
        """Обработчик для всех необработанных исключений"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Произошла непредвиденная ошибка",
                "error_code": "application.unexpected_error",
                "context": {"error_type": type(exc).__name__}
            }
        ) 