from sqlalchemy import Table, Column, Integer, String, DateTime, Text, func
from .base import metadata
from app.application.constants import Limits

# Таблица определений достижений
achievements_table = Table(
	'achievements',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('type', String(Limits.ACHIEVEMENT_TYPE_MAX_LENGTH), unique=True,
	       nullable=False),
	Column('name', String(Limits.ACHIEVEMENT_NAME_MAX_LENGTH), nullable=False),
	Column('description', Text),
	Column('points', Integer, default=0),
	Column('condition_field', String(Limits.ACHIEVEMENT_TYPE_MAX_LENGTH),
	       nullable=False),
	Column('condition_value', Integer, nullable=False),
	Column('created_at', DateTime, server_default=func.now())
)
