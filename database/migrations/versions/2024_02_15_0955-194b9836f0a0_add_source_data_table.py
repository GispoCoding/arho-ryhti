"""add_source_data_table

Revision ID: 194b9836f0a0
Revises: 7de05df06dce
Create Date: 2024-02-15 09:55:59.456659

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "194b9836f0a0"
down_revision: Union[str, None] = "7de05df06dce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "source_data",
        sa.Column("type_of_source_data_id", sa.UUID(), nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column(
            "language",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("additional_information_uri", sa.String(), nullable=False),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["type_of_source_data_id"],
            ["codes.type_of_source_data.id"],
            name="type_of_source_data_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("source_data", schema="hame")
    # ### end Alembic commands ###
