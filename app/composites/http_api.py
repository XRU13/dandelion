from fastapi import FastAPI
from app.adapters.http_api.controllers import (
    event_controller,
    user_controller, 
    achievement_controller,
    stats_controller
)
from app.adapters.http_api.exceptions import ExceptionHandler
from app.application.services.user_service import UserNotFoundError, UserScoreNotFoundError
from app.application.services.stats_service import UserNotFoundError as StatsUserNotFoundError
from app.application.services.achievement_service import AchievementServiceError
from app.application.services.event_service import (
    UserNotFoundError as EventUserNotFoundError,
    InvalidEventDataError,
    EventServiceError
)

# Композит HTTP API - точка входа приложения
def create_app() -> FastAPI:
    """Создает и настраивает FastAPI приложение"""
    app = FastAPI(
        title="Gaming Achievement System",
        description="API для игровой системы событий и достижений",
        version="1.0.0"
    )
    
    # Регистрируем обработчики исключений
    app.add_exception_handler(UserNotFoundError, ExceptionHandler.user_not_found_handler)
    app.add_exception_handler(UserScoreNotFoundError, ExceptionHandler.user_score_not_found_handler)
    app.add_exception_handler(StatsUserNotFoundError, ExceptionHandler.stats_user_not_found_handler)
    app.add_exception_handler(EventUserNotFoundError, ExceptionHandler.event_user_not_found_handler)
    app.add_exception_handler(InvalidEventDataError, ExceptionHandler.invalid_event_data_handler)
    app.add_exception_handler(AchievementServiceError, ExceptionHandler.achievement_service_error_handler)
    app.add_exception_handler(EventServiceError, ExceptionHandler.event_service_error_handler)
    app.add_exception_handler(RuntimeError, ExceptionHandler.runtime_error_handler)
    
    # Регистрируем все контроллеры напрямую с префиксом /api/v1
    app.include_router(event_controller.router, prefix="/api/v1")
    app.include_router(user_controller.router, prefix="/api/v1") 
    app.include_router(achievement_controller.router, prefix="/api/v1")
    app.include_router(stats_controller.router, prefix="/api/v1")
    
    @app.get("/")
    def read_root():
        return {
            "message": "Gaming Achievement System API",
            "version": "1.0.0",
            "docs": "/docs",
            "endpoints": {
                "events": "/api/v1/event",
                "users": "/api/v1/users", 
                "achievements": "/api/v1/achievements",
                "stats": "/api/v1/stats"
            }
        }
    
    return app

# Экспортируем готовое приложение
app = create_app() 