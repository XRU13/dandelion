from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, func
from .base import metadata

# Таблица счетов пользователей
user_scores_table = Table(
	'user_scores',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('user_id', Integer, ForeignKey('users.id'), unique=True,
	       nullable=False),
	Column('login_count', Integer, default=0),
	Column('levels_completed', Integer, default=0),
	Column('secrets_found', Integer, default=0),
	Column('updated_at', DateTime(timezone=True), server_default=func.now(),
	       onupdate=func.now())
)
