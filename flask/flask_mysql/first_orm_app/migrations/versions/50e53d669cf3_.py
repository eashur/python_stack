"""empty message

Revision ID: 50e53d669cf3
Revises: 4118dee0cd39
Create Date: 2019-04-17 17:02:30.672576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50e53d669cf3'
down_revision = '4118dee0cd39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=45), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=45), nullable=True),
    sa.Column('email', sa.VARCHAR(length=45), nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###
