"""Add phone column to user table

Revision ID: ccdc65098e54
Revises: 5125512988bf
Create Date: 2018-04-28 17:58:41.008860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccdc65098e54'
down_revision = '5125512988bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column('phone', sa.String(length=128), nullable=True)
    )


def downgrade():
    op.drop_column('user', 'phone')
