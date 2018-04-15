"""empty message

Revision ID: 22846df9cc96
Revises: d2f6233bf46f
Create Date: 2018-04-15 17:56:23.913368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22846df9cc96'
down_revision = 'd2f6233bf46f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('guid', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=1000), nullable=False),
    sa.Column('password_secret', sa.String(length=100), nullable=False),
    sa.Column('confirm_code', sa.String(length=6), nullable=True),
    sa.Column('fullname', sa.String(length=1000), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('guid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
