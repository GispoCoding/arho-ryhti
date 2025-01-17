"""add events to lifecycle statuses

Revision ID: 78dc89b6afaa
Revises: 4e68b614ba99
Create Date: 2025-01-13 15:20:42.512023

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "78dc89b6afaa"
down_revision: Union[str, None] = "4e68b614ba99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event_association",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("lifecycle_status_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "name_of_plan_case_decision_id",
            sa.UUID(as_uuid=False),
            nullable=True,
        ),
        sa.Column(
            "type_of_processing_event_id",
            sa.UUID(as_uuid=False),
            nullable=True,
        ),
        sa.Column(
            "type_of_interaction_event_id",
            sa.UUID(as_uuid=False),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["lifecycle_status_id"],
            ["codes.lifecycle_status.id"],
            name="lifecycle_status_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["name_of_plan_case_decision_id"],
            ["codes.name_of_plan_case_decision.id"],
            name="name_of_plan_case_decision_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_interaction_event_id"],
            ["codes.type_of_interaction_event.id"],
            name="type_of_interaction_event_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_processing_event_id"],
            ["codes.type_of_processing_event.id"],
            name="type_of_processing_event_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_event_association_lifecycle_status_id"),
        "event_association",
        ["lifecycle_status_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_event_association_name_of_plan_case_decision_id"),
        "event_association",
        ["name_of_plan_case_decision_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_event_association_type_of_interaction_event_id"),
        "event_association",
        ["type_of_interaction_event_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_event_association_type_of_processing_event_id"),
        "event_association",
        ["type_of_processing_event_id"],
        unique=False,
        schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_codes_event_association_type_of_processing_event_id"),
        table_name="event_association",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_event_association_type_of_interaction_event_id"),
        table_name="event_association",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_event_association_name_of_plan_case_decision_id"),
        table_name="event_association",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_event_association_lifecycle_status_id"),
        table_name="event_association",
        schema="codes",
    )
    op.drop_table("event_association", schema="codes")
    # ### end Alembic commands ###
