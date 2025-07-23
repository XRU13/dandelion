import logging

from celery.exceptions import Retry
from app.adapters.celery.config import celery_app, run_async, CelerySession
from app.adapters.database.repositories import (
    EventRepository,
    AchievementRepository,
    UserAchievementRepository,
    UserScoreRepository,
)
from app.adapters.cache.redis_repository import RedisUserScoreRepository
from app.application.utils import ScoreCalculator, AchievementChecker
from app.application.entities import UserAchievement, UserScore, EventType
from app.application.constants import CacheSettings

logger = logging.getLogger(__name__)


class LockBusyError(Exception):
    """Повтор ретрая, когда Redis‑блокировка занята."""
    pass


@celery_app.task(bind=True, max_retries=5)
def process_event(self, event_id: int):
    try:
        return run_async(_process_event_async, event_id)
    except LockBusyError as e:
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
    except Exception as e:
        logger.error(f"Error in process_event task: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60)


async def _process_event_async(CelerySession, event_id: int):
    redis_repo = RedisUserScoreRepository()
    lock_key = None

    async with CelerySession() as session:
        event_repo = EventRepository(session)
        score_repo = UserScoreRepository(session)
        achievement_repo = AchievementRepository(session)
        user_achievement_repo = UserAchievementRepository(session)

        # Читаем событие
        event = await event_repo.get_by_id(event_id)
        if not event:
            logger.warning(f"Event {event_id} not found")
            return

        user_id = event.user_id

        # Ставим Redis‑блокировку
        lock_key = f"lock:user_score:{user_id}"
        locked = await redis_repo.redis.set(lock_key, "1", nx=True, ex=30)
        if not locked:
            logger.info(f"Lock for user {user_id} is busy, retrying later")
            raise LockBusyError()

        # Получаем или создаём запись user_score
        user_score = await score_repo.get_by_user_id(user_id)
        if not user_score:
            user_score = UserScore(
                user_id=user_id,
                login_count=0,
                levels_completed=0,
                secrets_found=0,
            )
            await score_repo.create(user_score)

        # Обновляем счётчики
        if event.event_type == EventType.LOGIN.value:
            user_score.login_count += 1
        elif event.event_type == EventType.COMPLETE_LEVEL.value:
            user_score.levels_completed += 1
            lvl = event.details.get("level_id", 0) if event.details else 0
            # points рассчитывается внутри ScoreCalculator
        else:  # find_secret
            user_score.secrets_found += 1

        await score_repo.update(user_score)

        # Сохраняем в Redis и очищаем кэш /stats
        total_score = ScoreCalculator.calculate_total_score(user_score)
        await redis_repo.redis.set(
            f"user:{user_id}:score",
            total_score,
            ex=CacheSettings.DEFAULT_TTL,
        )
        await redis_repo.redis.delete(CacheSettings.get_stats_key(user_id))

        # Проверяем достижения
        all_achievements = await achievement_repo.get_all()
        existing = await user_achievement_repo.get_by_user_id(user_id)
        earned_ids = AchievementChecker.get_earned_achievement_ids(existing)

        new_achievements = []
        for ach in all_achievements:
            if (
                ach.id not in earned_ids
                and AchievementChecker.check_achievement_condition(ach, user_score)
            ):
                session.add(
                    UserAchievement(
                        user_id=user_id,
                        achievement_id=ach.id,
                    )
                )
                new_achievements.append(ach.name)

        # Фиксируем все изменения в БД
        await session.commit()

        # Отправляем уведомления
        for name in new_achievements:
            send_achievement_notification.delay(user_id, name)

    # Снимаем блокировку
    if lock_key:
        await redis_repo.redis.delete(lock_key)


@celery_app.task(name="send_achievement_notification")
def send_achievement_notification(user_id: int, achievement_name: str):
    logger.info(f"[Achievement] User #{user_id} unlocked '{achievement_name}'")
