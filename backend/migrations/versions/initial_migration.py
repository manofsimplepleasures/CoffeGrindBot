"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создание таблицы brew_methods
    op.create_table(
        'brew_methods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Создание таблицы grinders
    op.create_table(
        'grinders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'model', name='uq_grinder_name_model')
    )

    # Создание таблицы grind_settings
    op.create_table(
        'grind_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('brew_method_id', sa.Integer(), nullable=False),
        sa.Column('grinder_id', sa.Integer(), nullable=False),
        sa.Column('clicks', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['brew_method_id'], ['brew_methods.id'], ),
        sa.ForeignKeyConstraint(['grinder_id'], ['grinders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('brew_method_id', 'grinder_id', name='uq_grind_setting_method_grinder')
    )

    # Создание таблицы user_logs
    op.create_table(
        'user_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('brew_method_id', sa.Integer(), nullable=False),
        sa.Column('grinder_id', sa.Integer(), nullable=False),
        sa.Column('clicks', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['brew_method_id'], ['brew_methods.id'], ),
        sa.ForeignKeyConstraint(['grinder_id'], ['grinders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Создание индексов
    op.create_index('ix_user_logs_user_id', 'user_logs', ['user_id'])
    op.create_index('ix_user_logs_created_at', 'user_logs', ['created_at'])


def downgrade():
    # Удаление индексов
    op.drop_index('ix_user_logs_created_at')
    op.drop_index('ix_user_logs_user_id')

    # Удаление таблиц
    op.drop_table('user_logs')
    op.drop_table('grind_settings')
    op.drop_table('grinders')
    op.drop_table('brew_methods') 