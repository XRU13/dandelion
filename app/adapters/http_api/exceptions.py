from fastapi import Request, status
from fastapi.responses import JSONResponse
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


class ExceptionHandler:
	"""Централизованный обработчик исключений"""

	@staticmethod
	def _create_error_response(status_code: int, exception):
		"""Создает стандартный JSON ответ для исключения"""
		return JSONResponse(
			status_code=status_code,
			content={
				"detail": str(exception),
				"error_code": exception.code,
				"context": getattr(exception, 'context', {})
			}
		)

	@staticmethod
	async def user_not_found_handler(request: Request, exc: UserNotFoundError):
		return ExceptionHandler._create_error_response(
			status.HTTP_404_NOT_FOUND, exc)

	@staticmethod
	async def user_score_not_found_handler(request: Request,
	                                       exc: UserScoreNotFoundError):
		return ExceptionHandler._create_error_response(
			status.HTTP_404_NOT_FOUND, exc)

	@staticmethod
	async def event_not_found_handler(request: Request,
	                                  exc: EventNotFoundError):
		return ExceptionHandler._create_error_response(
			status.HTTP_404_NOT_FOUND, exc)

	@staticmethod
	async def invalid_event_data_handler(request: Request,
	                                     exc: InvalidEventDataError):
		return ExceptionHandler._create_error_response(
			status.HTTP_400_BAD_REQUEST, exc)

	@staticmethod
	async def validation_error_handler(request: Request, exc: ValidationError):
		return ExceptionHandler._create_error_response(
			status.HTTP_422_UNPROCESSABLE_ENTITY, exc)

	@staticmethod
	async def event_service_error_handler(request: Request,
	                                      exc: EventServiceError):
		return ExceptionHandler._create_error_response(
			status.HTTP_500_INTERNAL_SERVER_ERROR, exc)

	@staticmethod
	async def achievement_service_error_handler(request: Request,
	                                            exc: AchievementServiceError):
		return ExceptionHandler._create_error_response(
			status.HTTP_500_INTERNAL_SERVER_ERROR, exc)

	@staticmethod
	async def stats_service_error_handler(request: Request,
	                                      exc: StatsServiceError):
		return ExceptionHandler._create_error_response(
			status.HTTP_500_INTERNAL_SERVER_ERROR, exc)

	@staticmethod
	async def user_already_exists_handler(request: Request,
	                                      exc: UserAlreadyExistsError):
		return ExceptionHandler._create_error_response(
			status.HTTP_409_CONFLICT, exc
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
