"""Add user.displayname column

Revision ID: 1c0a47692aad
Revises: ff3fc27cd408
Create Date: 2025-10-31 08:45:45.282922

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1c0a47692aad"
down_revision: Union[str, Sequence[str], None] = "ff3fc27cd408"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("displayname", sa.String))
    op.execute(sa.text('UPDATE "user" SET displayname = username'))
    op.alter_column("user", "displayname", existing_type=sa.String(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "displayname")
