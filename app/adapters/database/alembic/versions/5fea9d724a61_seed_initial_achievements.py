"""seed_initial_achievements

Revision ID: 5fea9d724a61
Revises: d90c0856666d
Create Date: 2025-07-19 10:18:17.942648

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fea9d724a61'
down_revision: Union[str, None] = 'd90c0856666d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу для вставки данных
    achievements_table = sa.table(
        'achievements',
        sa.column('type', sa.String),
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('points', sa.Integer),
        sa.column('condition_field', sa.String),
        sa.column('condition_value', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )
    
    # Добавляем начальные достижения
    now = datetime.utcnow()
    
    op.bulk_insert(achievements_table, [
        {
            'type': 'newcomer',
            'name': 'Новичок',
            'description': 'Первый вход в игру',
            'points': 5,
            'condition_field': 'login_count',
            'condition_value': 1,
            'created_at': now
        },
        {
            'type': 'regular',
            'name': 'Постоянный игрок',
            'description': '5 входов в игру',
            'points': 25,
            'condition_field': 'login_count',
            'condition_value': 5,
            'created_at': now
        },
        {
            'type': 'veteran',
            'name': 'Ветеран',
            'description': '10 входов в игру',
            'points': 50,
            'condition_field': 'login_count',
            'condition_value': 10,
            'created_at': now
        },
        {
            'type': 'explorer',
            'name': 'Исследователь',
            'description': 'Найти 3 секретных объекта',
            'points': 30,
            'condition_field': 'secrets_found',
            'condition_value': 3,
            'created_at': now
        },
        {
            'type': 'treasure_hunter',
            'name': 'Охотник за сокровищами',
            'description': 'Найти 10 секретных объектов',
            'points': 100,
            'condition_field': 'secrets_found',
            'condition_value': 10,
            'created_at': now
        },
        {
            'type': 'secret_master',
            'name': 'Мастер секретов',
            'description': 'Найти 25 секретных объектов',
            'points': 250,
            'condition_field': 'secrets_found',
            'condition_value': 25,
            'created_at': now
        },
        {
            'type': 'beginner',
            'name': 'Начинающий',
            'description': 'Завершить 1 уровень',
            'points': 10,
            'condition_field': 'levels_completed',
            'condition_value': 1,
            'created_at': now
        },
        {
            'type': 'achiever',
            'name': 'Достигатор',
            'description': 'Завершить 5 уровней',
            'points': 75,
            'condition_field': 'levels_completed',
            'condition_value': 5,
            'created_at': now
        },
        {
            'type': 'master',
            'name': 'Мастер',
            'description': 'Завершить 10 уровней',
            'points': 200,
            'condition_field': 'levels_completed',
            'condition_value': 10,
            'created_at': now
        },
        {
            'type': 'champion',
            'name': 'Чемпион',
            'description': 'Завершить 25 уровней',
            'points': 500,
            'condition_field': 'levels_completed',
            'condition_value': 25,
            'created_at': now
        }
    ])


def downgrade() -> None:
    # Удаляем все добавленные достижения
    op.execute("DELETE FROM achievements WHERE type IN ('newcomer', 'regular', 'veteran', 'explorer', 'treasure_hunter', 'secret_master', 'beginner', 'achiever', 'master', 'champion')")
