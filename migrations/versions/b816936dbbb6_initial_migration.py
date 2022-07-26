"""Initial migration.

Revision ID: b816936dbbb6
Revises: 5332cc8837a3
Create Date: 2022-02-18 13:53:06.903990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b816936dbbb6'
down_revision = '5332cc8837a3'
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
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('buyer_tel', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=800), nullable=False),
    sa.Column('count', sa.String(length=200), nullable=False),
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
