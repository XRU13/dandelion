from sqlalchemy import Table, Column, Integer, String, DateTime, JSON, ForeignKey, func
from .base import metadata

# Таблица событий
events_table = Table(
    'events',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('event_type', String(50), nullable=False),
    Column('details', JSON),
    Column('created_at', DateTime, server_default=func.now())
) 