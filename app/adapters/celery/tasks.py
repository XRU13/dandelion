import asyncio
import logging
from app.adapters.celery.config import celery_app
from app.adapters.database.session import AsyncSessionLocal
from app.adapters.database.repositories import (
    EventRepository,
    UserScoreRepository,
    AchievementRepository,
    UserAchievementRepository
)
from app.adapters.cache.redis_repository import RedisUserScoreRepository
from app.application.entities import UserScore, UserAchievement
from app.application.utils import ScoreCalculator, AchievementChecker
from app.application.constants import Messages

logger = logging.getLogger(__name__)


@celery_app.task(name="process_event")
def process_event(event_id: int):
    """Обработка события"""
    
    async def _process_event():
        try:
            logger.info(f"Processing event {event_id}")
            
            # Создаем отдельную сессию для Celery
            async with AsyncSessionLocal() as session:
                try:
                    # Создаем репозитории
                    event_repo = EventRepository(session)
                    user_score_repo = UserScoreRepository(session)
                    achievement_repo = AchievementRepository(session)
                    user_achievement_repo = UserAchievementRepository(session)
                    redis_cache = RedisUserScoreRepository()
                    
                    # 1. Получаем событие
                    event = await event_repo.get_by_id(event_id)
                    if not event:
                        error_msg = f"Событие {event_id} не найдено"
                        logger.warning(error_msg)
                        return error_msg
                    
                    # 2. Рассчитываем очки за событие
                    points = ScoreCalculator.calculate_event_points(event.event_type)
                    logger.debug(f"Event type: {event.event_type}, points: {points}")
                    
                    # 3. Обновляем счет пользователя в БД
                    user_score = await user_score_repo.get_by_user_id(event.user_id)
                    if not user_score:
                        # Создаем новый счет
                        user_score = UserScore(
                            user_id=event.user_id,
                            login_count=0,
                            levels_completed=0,
                            secrets_found=0
                        )
                        user_score = await user_score_repo.create(user_score)
                    
                    # Обновляем счетчики с помощью утилиты
                    ScoreCalculator.update_user_score_counters(user_score, event.event_type)
                    await user_score_repo.update(user_score)
                    
                    # 4. Рассчитываем общий счет
                    total_score = ScoreCalculator.calculate_total_score(user_score)
                    
                    logger.debug(f"User stats - logins: {user_score.login_count}, levels: {user_score.levels_completed}, secrets: {user_score.secrets_found}, total: {total_score}")
                    
                    # 5. Проверяем достижения
                    all_achievements = await achievement_repo.get_all()
                    user_achievements = await user_achievement_repo.get_by_user_id(event.user_id)
                    earned_achievement_ids = AchievementChecker.get_earned_achievement_ids(user_achievements)
                    
                    new_achievements = []
                    for achievement in all_achievements:
                        if achievement.id in earned_achievement_ids:
                            continue
                        
                        # Проверяем условие достижения с помощью утилиты
                        if AchievementChecker.check_achievement_condition(achievement, user_score):
                            # Присваиваем достижение
                            user_achievement = UserAchievement(
                                user_id=event.user_id,
                                achievement_id=achievement.id
                            )
                            await user_achievement_repo.create(user_achievement)
                            new_achievements.append(achievement)
                            logger.info(f"Earned achievement: {achievement.name}")
                    
                    # 6. Обновляем Redis кэш
                    try:
                        await redis_cache.set_score(event.user_id, total_score)
                        logger.debug(f"Redis cache updated for user {event.user_id}")
                    except Exception as redis_error:
                        logger.warning(f"Failed to update Redis cache: {redis_error}")
                    
                    # Коммитим все изменения
                    await session.commit()
                    
                    # Формируем результат с использованием констант
                    result = Messages.EVENT_PROCESSING_SUCCESS.format(
                        event_id=event_id, 
                        points=points, 
                        total_score=total_score
                    )
                    if new_achievements:
                        achievement_names = [a.name for a in new_achievements]
                        result += f", new achievements: {', '.join(achievement_names)}"
                    
                    logger.info(result)
                    return result
                    
                except Exception as e:
                    await session.rollback()
                    raise e
                
        except Exception as e:
            error_msg = Messages.EVENT_PROCESSING_ERROR.format(event_id=event_id, error=str(e))
            logger.error(error_msg, exc_info=True)
            return error_msg
    
    # Запускаем асинхронную обработку
    return asyncio.run(_process_event()) 