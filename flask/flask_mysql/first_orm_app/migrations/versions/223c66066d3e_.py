"""empty message

Revision ID: 223c66066d3e
Revises: 50e53d669cf3
Create Date: 2019-04-17 17:41:22.898420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '223c66066d3e'
down_revision = '50e53d669cf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('age', sa.String(length=45), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'age')
    # ### end Alembic commands ###
