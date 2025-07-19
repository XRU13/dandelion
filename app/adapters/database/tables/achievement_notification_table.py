from sqlalchemy import Table, Column, Integer, DateTime, Boolean, Text, ForeignKey, func
from .base import metadata

# Таблица уведомлений о достижениях
achievement_notifications_table = Table(
    'achievement_notifications',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('achievement_id', Integer, ForeignKey('achievements.id'), nullable=False),
    Column('message', Text, nullable=False),
    Column('is_sent', Boolean, default=False),
    Column('created_at', DateTime, server_default=func.now()),
    Column('sent_at', DateTime)
) 