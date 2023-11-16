"""add created at and published column to post table

Revision ID: 79b8dbcc4411
Revises: bd2a63ffa398
Create Date: 2023-11-16 07:19:45.253619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79b8dbcc4411'
down_revision: Union[str, None] = 'bd2a63ffa398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published",sa.Boolean(),server_default="True"),)
    op.add_column('posts', sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,
                                     server_default=sa.text('now()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts", 'published')
    op.drop_column('posts', 'created_at')
    pass
