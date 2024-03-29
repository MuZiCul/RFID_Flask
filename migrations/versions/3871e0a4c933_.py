"""empty message

Revision ID: 3871e0a4c933
Revises: 
Create Date: 2024-01-10 14:54:27.993411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3871e0a4c933'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Inventory_notification_thresholds', sa.Integer(), nullable=True),
    sa.Column('notification', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inbound',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rfid', sa.String(length=200), nullable=True),
    sa.Column('num', sa.String(length=200), nullable=True),
    sa.Column('batch', sa.String(length=200), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('num', sa.String(length=200), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rfid', sa.String(length=200), nullable=True),
    sa.Column('warehouse', sa.String(length=200), nullable=True),
    sa.Column('Shelves', sa.String(length=200), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outbound',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rfid', sa.String(length=200), nullable=True),
    sa.Column('num', sa.String(length=200), nullable=True),
    sa.Column('batch', sa.String(length=200), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('outbound')
    op.drop_table('location')
    op.drop_table('inventory')
    op.drop_table('inbound')
    op.drop_table('config')
    # ### end Alembic commands ###
