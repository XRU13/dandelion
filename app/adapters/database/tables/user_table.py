from sqlalchemy import Table, Column, Integer, String, DateTime, func
from .base import metadata

# Таблица пользователей
users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True, nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('created_at', DateTime, server_default=func.now()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
) 