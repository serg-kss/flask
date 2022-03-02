"""Initial migration.

Revision ID: c4eed748444c
Revises: b6019a5708a6
Create Date: 2022-02-17 15:52:57.907258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4eed748444c'
down_revision = 'b6019a5708a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.String(length=30), nullable=False),
    sa.Column('date', sa.String(length=30), nullable=False),
    sa.Column('code_of_item', sa.String(length=200), nullable=False),
    sa.Column('buyer_data', sa.String(length=200), nullable=False),
    sa.Column('buyer_tel', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=800), nullable=False),
    sa.Column('price', sa.String(length=800), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('delivery', sa.String(length=30), nullable=False),
    sa.Column('payment', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
