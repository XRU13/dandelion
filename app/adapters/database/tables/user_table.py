from sqlalchemy import Table, Column, Integer, String, DateTime, func
from .base import metadata
from app.application.constants import Limits

# Таблица пользователей
users_table = Table(
	'users',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('username', String(Limits.USERNAME_MAX_LENGTH), unique=True,
	       nullable=False),
	Column('email', String(Limits.EMAIL_MAX_LENGTH), unique=True,
	       nullable=False),
	Column('created_at', DateTime, server_default=func.now()),
	Column('updated_at', DateTime, server_default=func.now(),
	       onupdate=func.now())
)
