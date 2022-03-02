"""Initial migration.

Revision ID: 4d2276f755a2
Revises: 2a7aac2fed6f
Create Date: 2022-02-17 15:31:47.907944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d2276f755a2'
down_revision = '2a7aac2fed6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code_of_item', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=800), nullable=False),
    sa.Column('price', sa.String(length=800), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('delivery', sa.String(length=30), nullable=False),
    sa.Column('payment', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###