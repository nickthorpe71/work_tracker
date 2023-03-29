"""Add work_type column to work_intervals table

Revision ID: aa04d66c62a5
Revises: 
Create Date: 2023-03-29 09:30:13.787654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'YYYYMMDD_HHMMSS'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('work_intervals', sa.Column('work_type', sa.String(), nullable=False, server_default='tmu'))


def downgrade():
    op.drop_column('work_intervals', 'work_type')