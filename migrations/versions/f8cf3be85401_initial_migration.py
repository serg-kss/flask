"""Initial migration.

Revision ID: f8cf3be85401
Revises: 86f2a0e6907a
Create Date: 2022-02-07 17:53:00.172173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8cf3be85401'
down_revision = '86f2a0e6907a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('изображение_товаров',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code_of_pic', sa.String(length=20), nullable=False),
    sa.Column('img', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('mimetype', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code_of_pic'),
    sa.UniqueConstraint('img')
    )
    op.create_table('товары',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code_of_item', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('price_fondy', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code_of_item')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('товары')
    op.drop_table('изображение_товаров')
    # ### end Alembic commands ###
