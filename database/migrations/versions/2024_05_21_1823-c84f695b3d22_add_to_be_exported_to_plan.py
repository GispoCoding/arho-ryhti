"""add to_be_exported to plan

Revision ID: c84f695b3d22
Revises: 0da11d97b6cb
Create Date: 2024-05-21 18:23:40.322147

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c84f695b3d22"
down_revision: Union[str, None] = "dba7f323b644"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan",
        sa.Column("to_be_exported", sa.Boolean(), server_default="f", nullable=False),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("plan", "to_be_exported", schema="hame")
    # ### end Alembic commands ###
