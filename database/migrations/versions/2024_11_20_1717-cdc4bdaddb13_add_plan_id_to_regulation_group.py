"""add plan_id to regulation group

Revision ID: cdc4bdaddb13
Revises: 626124880789
Create Date: 2024-11-20 17:17:16.166363

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_function import PGFunction

# revision identifiers, used by Alembic.
revision: str = "cdc4bdaddb13"
down_revision: Union[str, None] = "626124880789"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan_regulation_group",
        sa.Column(
            "plan_id",
            sa.UUID(as_uuid=False),
            nullable=True,
            comment="Plan to which this regulation group belongs",
        ),
        schema="hame",
    )

    # Update plan_id for existing plan regulation groups
    # Set the regulation group to the the first plan it is associated with
    op.execute(
        """
        UPDATE hame.plan_regulation_group
        SET plan_id = plan_ids.plan_id
        FROM
            (
                SELECT DISTINCT ON (plan_regulation_group_id)
                    rg.id plan_regulation_group_id,
                    COALESCE(
                        p.id,
                        lua.plan_id,
                        lup.plan_id,
                        l.plan_id,
                        oa.plan_id,
                        op.plan_id
                    ) plan_id
                FROM
                    hame.plan_regulation_group rg
                    LEFT JOIN hame.plan p
                        ON rg.id = p.plan_regulation_group_id
                    LEFT JOIN hame.land_use_area lua
                        ON rg.id = lua.plan_regulation_group_id
                    LEFT JOIN hame.land_use_point lup
                        ON rg.id = lup.plan_regulation_group_id
                    LEFT JOIN hame.line l
                        ON rg.id = l.plan_regulation_group_id
                    LEFT JOIN hame.other_area oa
                        ON rg.id = oa.plan_regulation_group_id
                    LEFT JOIN hame.other_point op
                        ON rg.id = op.plan_regulation_group_id
                ORDER BY 1, 2 NULLS LAST
            ) plan_ids
        WHERE plan_regulation_group.id = plan_ids.plan_regulation_group_id
        """
    )
    # We did our best to set the plan_id for each regulation group.
    # Delete the rest which are not associated with any plan.
    op.execute("""DELETE FROM hame.plan_regulation_group WHERE plan_id IS NULL""")
    op.alter_column(
        "plan_regulation_group",
        "plan_id",
        existing_type=sa.UUID(as_uuid=False),
        nullable=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_regulation_group_plan_id"),
        "plan_regulation_group",
        ["plan_id"],
        unique=False,
        schema="hame",
    )

    op.create_foreign_key(
        "plan_id_fkey",
        "plan_regulation_group",
        "plan",
        ["plan_id"],
        ["id"],
        source_schema="hame",
        referent_schema="hame",
        ondelete="CASCADE",
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "plan_id_fkey",
        "plan_regulation_group",
        schema="hame",
        type_="foreignkey",
    )
    op.drop_index(
        op.f("ix_hame_plan_regulation_group_plan_id"),
        table_name="plan_regulation_group",
        schema="hame",
    )
    op.drop_column("plan_regulation_group", "plan_id", schema="hame")
    # ### end Alembic commands ###
