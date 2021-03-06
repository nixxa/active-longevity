"""empty message

Revision ID: c8fe672be096
Revises: 22846df9cc96
Create Date: 2018-04-15 18:21:15.325238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8fe672be096'
down_revision = '22846df9cc96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('created', sa.DateTime(), nullable=False))
    op.create_unique_constraint(None, 'user', ['guid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'created')
    op.drop_column('user', 'confirmed')
    # ### end Alembic commands ###
