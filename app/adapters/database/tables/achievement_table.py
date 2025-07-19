from sqlalchemy import Table, Column, Integer, String, DateTime, Text, func
from .base import metadata

# Таблица определений достижений
achievements_table = Table(
    'achievements',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String(50), unique=True, nullable=False),
    Column('name', String(100), nullable=False),
    Column('description', Text),
    Column('points', Integer, default=0),
    Column('condition_field', String(50), nullable=False),
    Column('condition_value', Integer, nullable=False),
    Column('created_at', DateTime, server_default=func.now())
) 