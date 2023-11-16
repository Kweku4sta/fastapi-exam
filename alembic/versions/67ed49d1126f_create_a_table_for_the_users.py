"""create a table for the users

Revision ID: 67ed49d1126f
Revises: 154591891842
Create Date: 2023-11-16 03:43:54.133099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67ed49d1126f'
down_revision: Union[str, None] = '154591891842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id', sa.Integer(),nullable=False),
    sa.Column("email",sa.String(),nullable=False),sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=
                              sa.text('now()'),nullable=False), sa.PrimaryKeyConstraint("id"),sa.UniqueConstraint("email")
            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
