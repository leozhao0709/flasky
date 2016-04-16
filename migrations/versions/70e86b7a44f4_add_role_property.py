"""add role property

Revision ID: 70e86b7a44f4
Revises: 19356cb65dac
Create Date: 2016-04-15 18:27:15.814830

"""

# revision identifiers, used by Alembic.
revision = '70e86b7a44f4'
down_revision = '19356cb65dac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    ### end Alembic commands ###