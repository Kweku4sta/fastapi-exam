"""add content column to the post table

Revision ID: 154591891842
Revises: 736a2dda39b6
Create Date: 2023-11-16 03:30:47.030979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '154591891842'
down_revision: Union[str, None] = '736a2dda39b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
