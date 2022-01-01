"""add content table to post table

Revision ID: 910d5df161a4
Revises: 1ba22e01f335
Create Date: 2022-01-01 18:02:12.226381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910d5df161a4'
down_revision = '1ba22e01f335'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass