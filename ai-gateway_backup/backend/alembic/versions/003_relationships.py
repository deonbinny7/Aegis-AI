"""Relationships and cascade deletes

Revision ID: 003_relationships
Revises: 002_schema_refinement
Create Date: 2026-06-29 12:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003_relationships'
down_revision: Union[str, None] = '002_schema_refinement'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # messages
    op.add_column('messages', sa.Column('prompt_version_id', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('experiment_id', sa.String(), nullable=True))
    
    # We must drop the old foreign keys and recreate them with ondelete rules
    op.drop_constraint('messages_session_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key('messages_session_id_fkey', 'messages', 'sessions', ['session_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('messages_prompt_version_id_fkey', 'messages', 'prompt_versions', ['prompt_version_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('messages_experiment_id_fkey', 'messages', 'experiments', ['experiment_id'], ['id'], ondelete='SET NULL')

    # sessions
    op.drop_constraint('sessions_user_id_fkey', 'sessions', type_='foreignkey')
    op.create_foreign_key('sessions_user_id_fkey', 'sessions', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # sessions
    op.drop_constraint('sessions_user_id_fkey', 'sessions', type_='foreignkey')
    op.create_foreign_key('sessions_user_id_fkey', 'sessions', 'users', ['user_id'], ['id'])

    # messages
    op.drop_constraint('messages_experiment_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_prompt_version_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_session_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key('messages_session_id_fkey', 'messages', 'sessions', ['session_id'], ['id'])
    
    op.drop_column('messages', 'experiment_id')
    op.drop_column('messages', 'prompt_version_id')
