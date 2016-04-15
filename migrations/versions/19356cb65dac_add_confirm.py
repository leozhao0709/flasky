"""add confirm

Revision ID: 19356cb65dac
Revises: df9df093dc11
Create Date: 2016-04-14 16:37:31.453160

"""

# revision identifiers, used by Alembic.
revision = '19356cb65dac'
down_revision = 'df9df093dc11'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###