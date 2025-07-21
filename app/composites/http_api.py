from fastapi import FastAPI
from app.adapters.http_api.controllers import (
	event_controller,
	user_controller,
	achievement_controller,
	stats_controller
)
from app.adapters.http_api.exceptions import ExceptionHandler
from app.application.exceptions import (
	UserNotFoundError,
	UserScoreNotFoundError,
	EventNotFoundError,
	InvalidEventDataError,
	EventServiceError,
	AchievementServiceError,
	StatsServiceError,
	ValidationError,
	UserAlreadyExistsError,
)


# Композит HTTP API - точка входа приложения
def create_app() -> FastAPI:
	"""Создает и настраивает FastAPI приложение"""
	app = FastAPI(
		title="Gaming Achievement System",
		description="API для игровой системы событий и достижений",
		version="1.0.0"
	)

	# Регистрируем обработчики исключений с приоритетом (специфичные первыми)

	# 404 Not Found
	app.add_exception_handler(UserNotFoundError,
	                          ExceptionHandler.user_not_found_handler)
	app.add_exception_handler(UserScoreNotFoundError,
	                          ExceptionHandler.user_score_not_found_handler)
	app.add_exception_handler(EventNotFoundError,
	                          ExceptionHandler.event_not_found_handler)

	# 400 Bad Request
	app.add_exception_handler(InvalidEventDataError,
	                          ExceptionHandler.invalid_event_data_handler)

	# 422 Validation Error
	app.add_exception_handler(ValidationError,
	                          ExceptionHandler.validation_error_handler)

	# 500 Internal Server Error
	app.add_exception_handler(EventServiceError,
	                          ExceptionHandler.event_service_error_handler)
	app.add_exception_handler(AchievementServiceError,
	                          ExceptionHandler.achievement_service_error_handler)
	app.add_exception_handler(StatsServiceError,
	                          ExceptionHandler.stats_service_error_handler)
	app.add_exception_handler(UserAlreadyExistsError,
	                          ExceptionHandler.user_already_exists_handler)

	# Общие обработчики (в конце)
	app.add_exception_handler(RuntimeError,
	                          ExceptionHandler.runtime_error_handler)
	app.add_exception_handler(Exception,
	                          ExceptionHandler.generic_exception_handler)

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
