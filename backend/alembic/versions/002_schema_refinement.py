"""Schema refinement for prompt 2

Revision ID: 002_schema_refinement
Revises: 001_initial
Create Date: 2026-06-29 12:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_schema_refinement'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.add_column('users', sa.Column('password_hash', sa.String(), nullable=False, server_default=''))
    op.alter_column('users', 'password_hash', server_default=None)
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    op.drop_column('users', 'hashed_password')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'username')

    # prompt_versions
    op.add_column('prompt_versions', sa.Column('variables', sa.JSON(), nullable=True))
    op.add_column('prompt_versions', sa.Column('tags', sa.JSON(), nullable=True))
    op.add_column('prompt_versions', sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True))
    op.drop_column('prompt_versions', 'parameters')

    # usage_logs
    op.add_column('usage_logs', sa.Column('cost_usd', sa.Float(), nullable=True))
    op.drop_column('usage_logs', 'cost')

    # experiments
    op.add_column('experiments', sa.Column('status', sa.String(), nullable=True))
    op.add_column('experiments', sa.Column('metric', sa.String(), nullable=True))
    op.add_column('experiments', sa.Column('split_pct', sa.Float(), nullable=True))
    op.drop_column('experiments', 'description')
    op.drop_column('experiments', 'is_active')
    op.drop_column('experiments', 'config')


def downgrade() -> None:
    # experiments
    op.add_column('experiments', sa.Column('config', sa.JSON(), nullable=True))
    op.add_column('experiments', sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True))
    op.add_column('experiments', sa.Column('description', sa.String(), nullable=True))
    op.drop_column('experiments', 'split_pct')
    op.drop_column('experiments', 'metric')
    op.drop_column('experiments', 'status')

    # usage_logs
    op.add_column('usage_logs', sa.Column('cost', sa.Float(), nullable=True))
    op.drop_column('usage_logs', 'cost_usd')

    # prompt_versions
    op.add_column('prompt_versions', sa.Column('parameters', sa.JSON(), nullable=True))
    op.drop_column('prompt_versions', 'is_active')
    op.drop_column('prompt_versions', 'tags')
    op.drop_column('prompt_versions', 'variables')

    # users
    op.add_column('users', sa.Column('username', sa.String(), nullable=False, server_default=''))
    op.alter_column('users', 'username', server_default=None)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False, server_default=''))
    op.alter_column('users', 'hashed_password', server_default=None)
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'password_hash')

# Refactored for performance polish — 2026-05-29T16:11:33

# Refactored for performance polish — 2026-06-14T20:55:52
