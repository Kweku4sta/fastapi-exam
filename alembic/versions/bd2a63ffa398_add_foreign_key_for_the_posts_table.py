"""add foreign key for the posts table

Revision ID: bd2a63ffa398
Revises: 67ed49d1126f
Create Date: 2023-11-16 04:08:20.214384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd2a63ffa398'
down_revision: Union[str, None] = '67ed49d1126f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users"
                          ,local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column('posts', "owner_id")
    pass
