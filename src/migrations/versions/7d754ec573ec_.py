"""empty message

Revision ID: 7d754ec573ec
Revises: 16148f264076
Create Date: 2018-04-22 19:20:02.829900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d754ec573ec'
down_revision = '16148f264076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('number', sa.VARCHAR(length=10), nullable=True))
    op.add_column('activity', sa.Column('week_schedule', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.create_unique_constraint(None, 'one_time_action', ['guid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'one_time_action', type_='unique')
    op.drop_column('activity', 'week_schedule')
    op.drop_column('activity', 'number')
    # ### end Alembic commands ###
