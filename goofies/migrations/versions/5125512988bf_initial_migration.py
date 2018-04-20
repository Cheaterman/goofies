"""Initial migration

Revision ID: 5125512988bf
Revises:
Create Date: 2018-04-20 16:34:01.411547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5125512988bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('price', sa.Numeric(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=128), nullable=False),
        sa.Column('last_name', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('company', sa.String(length=128), nullable=True),
        sa.Column('password', sa.String(length=64), nullable=False),
        sa.Column('active', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('activation_key', sa.String(length=64), nullable=False),
        sa.Column('admin', sa.Boolean(), server_default='0', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('buyer_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('payment_id', sa.String(length=128), nullable=True),
        sa.Column('paid', sa.Boolean(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['buyer_id'], ['user.id'],),
        sa.ForeignKeyConstraint(['item_id'], ['item.id'],),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('order')
    op.drop_table('user')
    op.drop_table('item')
