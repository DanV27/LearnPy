"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-06

Captures the three tables that existed before Flask-Migrate was added:
  - user
  - generation
  - lesson_progress
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'generation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('spec', sa.String(length=500), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('lesson_markdown', sa.Text(), nullable=True),
        sa.Column('code', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'lesson_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=80), nullable=False),
        sa.Column('viewed_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'slug', name='uq_lesson_progress_user_slug'),
    )
    op.create_index('ix_lesson_progress_user_id', 'lesson_progress', ['user_id'])
    op.create_index('ix_lesson_progress_slug',    'lesson_progress', ['slug'])


def downgrade():
    op.drop_index('ix_lesson_progress_slug',    table_name='lesson_progress')
    op.drop_index('ix_lesson_progress_user_id', table_name='lesson_progress')
    op.drop_table('lesson_progress')
    op.drop_table('generation')
    op.drop_table('user')
