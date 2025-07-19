import logging
from datetime import datetime
from app.application.entities import Event, EventType, UserScore
from app.application.interfaces import (
    IEventRepository, IUserScoreRepository, IUserRepository
)
from app.application.exceptions import (
    EventNotFoundError, UserNotFoundError, InvalidEventDataError, 
    EventServiceError
)
from app.application.utils import ScoreCalculator, ValidationHelper

logger = logging.getLogger(__name__)


class EventService:
    """Сервис для работы с событиями"""
    
    def __init__(
        self,
        event_repo: IEventRepository,
        user_score_repo: IUserScoreRepository,
        user_repo: IUserRepository,
        redis_cache=None
    ):
        self.event_repo = event_repo
        self.user_score_repo = user_score_repo
        self.user_repo = user_repo
        self.redis_cache = redis_cache
    
    async def process_event(self, user_id: int, event_type: EventType, details: dict | None = None) -> Event:
        """Обрабатывает событие пользователя"""
        try:
            # Валидация входных данных
            if not ValidationHelper.validate_user_id(user_id):
                raise InvalidEventDataError(details="Некорректный ID пользователя")
            
            if not ValidationHelper.validate_event_details(details):
                raise InvalidEventDataError(details="Некорректные детали события")
            
            # Проверяем, что пользователь существует
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            
            # Создаем событие
            event = Event(
                user_id=user_id,
                event_type=event_type,
                details=details
            )
            
            # Сохраняем событие
            event = await self.event_repo.create(event)
            
            # Обновляем счет пользователя и возвращаем заработанные очки
            points_earned = await self._update_user_score(user_id, event_type, details)
            
            # Обновляем кэш в Redis (если доступен)
            await self._update_redis_cache(user_id, event, points_earned)
            
            return event
            
        except Exception as e:
            if isinstance(e, (UserNotFoundError, InvalidEventDataError)):
                raise
            raise EventServiceError(error=str(e))
    
    async def _update_redis_cache(self, user_id: int, event: Event, points_earned: int) -> None:
        """Обновляет кэш Redis с обработкой ошибок"""
        if not self.redis_cache:
            return
        
        try:
            await self.redis_cache.increment_score(user_id, points_earned)
            await self.redis_cache.add_event(user_id, event)
            logger.debug(f"Redis cache updated for user {user_id}: +{points_earned} points")
        except Exception as e:
            # Логируем ошибку, но не прерываем выполнение
            logger.warning(f"Failed to update Redis cache for user {user_id}: {e}")
            # Можно также создать исключение для мониторинга
            # raise CacheUnavailableError(error=str(e))
    
    async def _update_user_score(self, user_id: int, event_type: EventType, details: dict | None) -> int:
        """Обновляет счет пользователя на основе события и возвращает заработанные очки"""
        
        # Получаем текущий счет пользователя
        user_score = await self.user_score_repo.get_by_user_id(user_id)
        
        if not user_score:
            # Создаем новый счет для пользователя
            user_score = UserScore(
                user_id=user_id,
                login_count=0,
                levels_completed=0,
                secrets_found=0
            )
            user_score = await self.user_score_repo.create(user_score)
        
        # Обновляем счетчики в зависимости от типа события
        ScoreCalculator.update_user_score_counters(user_score, event_type)
        
        # Обновляем время последнего изменения
        user_score.updated_at = datetime.utcnow()
        
        # Сохраняем изменения
        await self.user_score_repo.update(user_score)
        
        # Рассчитываем заработанные очки
        points_earned = ScoreCalculator.calculate_event_points(event_type)
        
        return points_earned
    
    async def create_event(self, user_id: int, event_type: EventType, details: dict | None = None) -> Event:
        """Создать новое событие"""
        try:
            # Проверяем, что пользователь существует
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            
            # Создаем событие
            event = Event(
                user_id=user_id,
                event_type=event_type,
                details=details
            )
            
            return await self.event_repo.create(event)
        except Exception as e:
            if isinstance(e, UserNotFoundError):
                raise
            raise EventServiceError(error=str(e))
    
    async def get_event_by_id(self, event_id: int) -> Event:
        """Получить событие по ID"""
        try:
            event = await self.event_repo.get_by_id(event_id)
            if not event:
                raise EventNotFoundError(event_id=event_id)
            return event
        except Exception as e:
            if isinstance(e, EventNotFoundError):
                raise
            raise EventServiceError(error=str(e))
    
    async def get_user_events(self, user_id: int) -> list[Event]:
        """Получить все события пользователя"""
        try:
            # Проверяем, что пользователь существует
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            
            return await self.event_repo.get_by_user_id(user_id)
        except Exception as e:
            if isinstance(e, UserNotFoundError):
                raise
            raise EventServiceError(error=str(e))
        