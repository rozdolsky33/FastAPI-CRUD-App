"""Set username and short description to not nullable

Revision ID: a782b76791a4
Revises: 83b39582f7bf
Create Date: 2022-10-17 01:33:31.215061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a782b76791a4'
down_revision = '83b39582f7bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", "username", nullable=False)
    op.alter_column("users", "short_description", nullable=False)
    # op.add_column("users", sa.Column("test", sa.String()))


def downgrade() -> None:
    op.alter_column("users", "short_description", nullable=False)
    op.alter_column("users", "username", nullable=False)
    # op.alter_column("users", "username", nullable=True)
