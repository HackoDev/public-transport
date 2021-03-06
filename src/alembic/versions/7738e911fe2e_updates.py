"""Updates

Revision ID: 7738e911fe2e
Revises: 86914cdb5ca1
Create Date: 2018-04-17 13:10:20.736043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7738e911fe2e'
down_revision = '86914cdb5ca1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('name', sa.String(length=256), nullable=False))
    op.alter_column('transports', 'driver_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transports', 'driver_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('routes', 'name')
    # ### end Alembic commands ###
