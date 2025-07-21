from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, func
from .base import metadata

# Таблица достижений пользователей
user_achievements_table = Table(
	'user_achievements',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
	Column('achievement_id', Integer, ForeignKey('achievements.id'),
	       nullable=False),
	Column('earned_at', DateTime, server_default=func.now())
)
