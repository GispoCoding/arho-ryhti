"""add legal effects of master plan

Revision ID: 82a732dbaebe
Revises: 2dbcbac65d4f
Create Date: 2025-02-24 14:26:55.837670

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "82a732dbaebe"
down_revision: Union[str, None] = "2dbcbac65d4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "legal_effects_of_master_plan",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), server_default="", nullable=False),
        sa.Column("name", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "description",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.legal_effects_of_master_plan.id"],
            name="legal_effects_of_master_plan_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_legal_effects_of_master_plan_level"),
        "legal_effects_of_master_plan",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_legal_effects_of_master_plan_parent_id"),
        "legal_effects_of_master_plan",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_legal_effects_of_master_plan_short_name"),
        "legal_effects_of_master_plan",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_legal_effects_of_master_plan_value"),
        "legal_effects_of_master_plan",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "legal_effects_association",
        sa.Column("plan_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "legal_effects_of_master_plan_id",
            sa.UUID(as_uuid=False),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["legal_effects_of_master_plan_id"],
            ["codes.legal_effects_of_master_plan.id"],
            name="legal_effects_of_master_plan_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["hame.plan.id"],
            name="plan_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("plan_id", "legal_effects_of_master_plan_id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_legal_effects_association_legal_effects_of_master_plan_id"),
        "legal_effects_association",
        ["legal_effects_of_master_plan_id"],
        unique=False,
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_hame_legal_effects_association_legal_effects_of_master_plan_id"),
        table_name="legal_effects_association",
        schema="hame",
    )
    op.drop_table("legal_effects_association", schema="hame")
    op.drop_index(
        op.f("ix_codes_legal_effects_of_master_plan_value"),
        table_name="legal_effects_of_master_plan",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_legal_effects_of_master_plan_short_name"),
        table_name="legal_effects_of_master_plan",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_legal_effects_of_master_plan_parent_id"),
        table_name="legal_effects_of_master_plan",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_legal_effects_of_master_plan_level"),
        table_name="legal_effects_of_master_plan",
        schema="codes",
    )
    op.drop_table("legal_effects_of_master_plan", schema="codes")
    # ### end Alembic commands ###
