"""empty message

Revision ID: 3107c18b8668
Revises: 
Create Date: 2019-07-31 13:15:11.117515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3107c18b8668'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'client',
        sa.Column('client_id', sa.String(30), primary_key=True),
        sa.Column('client_name', sa.String(30), nullable=False),
        sa.Column('client_secret', sa.String(30), nullable=False),
        sa.Column('status', sa.Boolean, nullable=False)
    )
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client')
    pass
    # ### end Alembic commands ###
