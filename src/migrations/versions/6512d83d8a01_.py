"""empty message

Revision ID: 6512d83d8a01
Revises: c8fe672be096
Create Date: 2018-04-16 21:29:14.874394

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6512d83d8a01'
down_revision = 'c8fe672be096'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    op.add_column('report', sa.Column('reporter_id', sa.String(length=100), nullable=True))
    op.create_foreign_key(None, 'report', 'user', ['reporter_id'], ['guid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'report', type_='foreignkey')
    op.drop_column('report', 'reporter_id')
    op.create_table('sessions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('session_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('expiry', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='sessions_pkey'),
    sa.UniqueConstraint('session_id', name='sessions_session_id_key')
    )
    # ### end Alembic commands ###
