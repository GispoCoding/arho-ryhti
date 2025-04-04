"""fix document fields

Revision ID: f5dad001cfff
Revises: 82a732dbaebe
Create Date: 2025-03-26 18:57:15.105413

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f5dad001cfff"
down_revision: Union[str, None] = "82a732dbaebe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document",
        sa.Column("accessibility", sa.Boolean(), nullable=False, server_default="0"),
        schema="hame",
    )
    op.alter_column(
        "document",
        "permanent_document_identifier",
        existing_type=sa.UUID(),
        type_=sa.String(),
        existing_nullable=True,
        schema="hame",
    )
    op.drop_column("document", "decision", schema="hame")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document",
        sa.Column("decision", sa.BOOLEAN(), autoincrement=False, nullable=False),
        schema="hame",
    )
    op.alter_column(
        "document",
        "permanent_document_identifier",
        existing_type=sa.String(),
        type_=sa.UUID(),
        existing_nullable=True,
        schema="hame",
        postgresql_using="permanent_document_identifier::uuid",
    )
    op.drop_column("document", "accessibility", schema="hame")
    # ### end Alembic commands ###
