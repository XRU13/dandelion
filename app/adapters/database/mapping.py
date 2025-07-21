from app.application.entities import (
	User,
	Event,
	UserScore,
	Achievement,
	UserAchievement,
	AchievementNotification,
)
from .tables import (
	mapper_registry,
	users_table,
	events_table,
	user_scores_table,
	achievements_table,
	user_achievements_table,
	achievement_notifications_table,
)


def configure_mappers():
	"""Настройка императивного маппинга"""

	# Маппинг пользователей
	mapper_registry.map_imperatively(User, users_table)

	# Маппинг событий
	mapper_registry.map_imperatively(Event, events_table)

	# Маппинг счетов пользователей
	mapper_registry.map_imperatively(UserScore, user_scores_table)

	# Маппинг достижений
	mapper_registry.map_imperatively(Achievement, achievements_table)

	# Маппинг достижений пользователей
	mapper_registry.map_imperatively(UserAchievement, user_achievements_table)

	# Маппинг уведомлений о достижениях
	mapper_registry.map_imperatively(
		AchievementNotification,
		achievement_notifications_table,
	)
