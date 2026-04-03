"""Prompt 3 Schema

Revision ID: prompt3_schema
Revises: adb37c7c2c62
Create Date: 2026-06-29 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'prompt3_schema'
down_revision = 'adb37c7c2c62'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # provider_pricing
    op.create_table('provider_pricing',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('model_name', sa.String(), nullable=False),
    sa.Column('input_price_per_token', sa.Float(), nullable=False, server_default='0.0'),
    sa.Column('output_price_per_token', sa.Float(), nullable=False, server_default='0.0'),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_pricing_provider'), 'provider_pricing', ['provider'], unique=False)
    op.create_index(op.f('ix_provider_pricing_model_name'), 'provider_pricing', ['model_name'], unique=False)

    # webhooks
    op.create_table('webhooks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('trigger_event', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webhooks_trigger_event'), 'webhooks', ['trigger_event'], unique=False)

    # provider_benchmarks
    op.create_table('provider_benchmarks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('model_name', sa.String(), nullable=False),
    sa.Column('availability_pct', sa.Float(), nullable=True),
    sa.Column('avg_latency_ms', sa.Float(), nullable=True),
    sa.Column('total_requests', sa.Integer(), nullable=True),
    sa.Column('failed_requests', sa.Integer(), nullable=True),
    sa.Column('throughput_tps', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_benchmarks_provider'), 'provider_benchmarks', ['provider'], unique=False)
    op.create_index(op.f('ix_provider_benchmarks_model_name'), 'provider_benchmarks', ['model_name'], unique=False)

    # audit_logs
    op.create_table('audit_logs',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('provider', sa.String(), nullable=True),
    sa.Column('prompt_version_id', sa.String(), nullable=True),
    sa.Column('experiment_id', sa.String(), nullable=True),
    sa.Column('session_id', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('retry_count', sa.Integer(), nullable=True),
    sa.Column('metadata', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_session_id'), 'audit_logs', ['session_id'], unique=False)

    # experiment_variants
    op.create_table('experiment_variants',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('experiment_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('config', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['experiment_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('experiment_variants')
    op.drop_table('audit_logs')
    op.drop_table('provider_benchmarks')
    op.drop_table('webhooks')
    op.drop_table('provider_pricing')
