"""empty message

Revision ID: 4da404bd36e1
Revises: 0e332bd57b7d
Create Date: 2016-04-11 00:14:48.069888

"""

# revision identifiers, used by Alembic.
revision = '4da404bd36e1'
down_revision = '0e332bd57b7d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('test', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'test')
    ### end Alembic commands ###