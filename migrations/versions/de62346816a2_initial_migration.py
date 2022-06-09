"""Initial migration.

Revision ID: de62346816a2
Revises: b816936dbbb6
Create Date: 2022-06-08 22:42:23.502455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de62346816a2'
down_revision = 'b816936dbbb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tовары', sa.Column('size', sa.String(length=50), nullable=True))
    op.add_column('Tовары', sa.Column('sezon', sa.String(length=20), nullable=True))
    op.add_column('Tовары', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('Tовары', sa.Column('country', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Tовары', 'country')
    op.drop_column('Tовары', 'year')
    op.drop_column('Tовары', 'sezon')
    op.drop_column('Tовары', 'size')
    # ### end Alembic commands ###