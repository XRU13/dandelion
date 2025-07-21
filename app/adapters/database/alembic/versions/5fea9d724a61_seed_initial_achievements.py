"""seed_initial_achievements

Revision ID: 5fea9d724a61
Revises: d90c0856666d
Create Date: 2025-07-19 10:18:17.942648
"""
from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa
from sqlalchemy import delete

revision: str = '5fea9d724a61'
down_revision: Union[str, None] = 'd90c0856666d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

now = datetime.now(timezone.utc)

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

initial_achievements = [
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
        'type': 'explorer',
        'name': 'Исследователь',
        'description': 'Найти 3 секретных объекта',
        'points': 50,
        'condition_field': 'secrets_found',
        'condition_value': 3,
        'created_at': now
    },
    {
        'type': 'master',
        'name': 'Мастер',
        'description': 'Завершить 10 уровней',
        'points': 20,
        'condition_field': 'levels_completed',
        'condition_value': 10,
        'created_at': now
    }
]

def upgrade() -> None:
    op.bulk_insert(achievements_table, initial_achievements)


def downgrade() -> None:
    stmt = delete(achievements_table).where(
        achievements_table.c.type.in_(['newcomer', 'explorer', 'master'])
    )
    op.execute(stmt)