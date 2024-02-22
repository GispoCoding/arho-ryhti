"""add_plan_regulation_table

Revision ID: 776ca8ea5a68
Revises: 6ee06a6e634a
Create Date: 2024-02-08 16:48:20.346350

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "776ca8ea5a68"
down_revision: Union[str, None] = "8f3c677fe184"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plan_regulation",
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
        sa.Column("type_of_plan_regulation_id", sa.UUID(), nullable=False),
        sa.Column("type_of_verbal_plan_regulation_id", sa.UUID(), nullable=False),
        sa.Column("numeric_range", postgresql.NUMRANGE(), nullable=False),
        sa.Column("unit", sa.String(), nullable=False),
        sa.Column(
            "text_value",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("numeric_value", sa.Float(), nullable=False),
        sa.Column(
            "regulation_number", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("exported_at", sa.DateTime(), nullable=True),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.Column("repealed_at", sa.DateTime(), nullable=True),
        sa.Column("lifecycle_status_id", sa.UUID(), nullable=False),
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
            ["lifecycle_status_id"],
            ["codes.lifecycle_status.id"],
            name="plan_lifecycle_status_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_plan_regulation_id"],
            ["codes.type_of_plan_regulation.id"],
            name="type_of_plan_regulation_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_verbal_plan_regulation_id"],
            ["codes.type_of_verbal_plan_regulation.id"],
            name="type_of_verbal_plan_regulation_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plan_regulation", schema="hame")
    # ### end Alembic commands ###
