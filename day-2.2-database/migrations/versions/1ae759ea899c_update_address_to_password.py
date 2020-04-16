"""update address to password

Revision ID: 1ae759ea899c
Revises: faed669a84fc
Create Date: 2020-04-16 17:20:58.662940

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1ae759ea899c'
down_revision = 'faed669a84fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('password', sa.String(length=255), nullable=True))
    op.drop_column('person', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('address', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('person', 'password')
    # ### end Alembic commands ###
