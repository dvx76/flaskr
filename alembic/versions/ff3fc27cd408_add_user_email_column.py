"""Add user.email column

Revision ID: ff3fc27cd408
Revises:
Create Date: 2025-10-30 09:22:49.718786

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ff3fc27cd408"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("email", sa.String))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "email")
