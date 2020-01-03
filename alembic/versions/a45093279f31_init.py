"""init

Revision ID: a45093279f31
Revises: 
Create Date: 2020-01-03 12:31:44.664257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'a45093279f31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('_password', sa.LargeBinary(length=60), nullable=True),
    sa.Column('pseudonym', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=func.datetime('now'), nullable=False),
    sa.Column('modified_at', sa.DateTime(), server_default=func.datetime('now'), onupdate=func.datetime('now'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    )
    op.create_table('books',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('price_in_eur', sa.DECIMAL(precision=9, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=func.datetime('now'), nullable=False),
    sa.Column('modified_at', sa.DateTime(), server_default=func.datetime('now'), onupdate=func.datetime('now'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('books')
    op.drop_table('users')
