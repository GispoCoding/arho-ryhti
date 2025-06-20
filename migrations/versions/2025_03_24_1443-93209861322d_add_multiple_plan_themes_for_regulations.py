"""add multiple plan themes for regulations

Revision ID: 93209861322d
Revises: 82a732dbaebe
Create Date: 2025-03-24 14:43:55.313834

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "93209861322d"
down_revision: Union[str, None] = "2010b7bcc3b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plan_theme_association",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("plan_regulation_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("plan_proposition_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("plan_theme_id", sa.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(
            ["plan_proposition_id"],
            ["hame.plan_proposition.id"],
            name="plan_proposition_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["plan_regulation_id"],
            ["hame.plan_regulation.id"],
            name="plan_regulation_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["plan_theme_id"],
            ["codes.plan_theme.id"],
            name="plan_theme_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_theme_association_plan_proposition_id"),
        "plan_theme_association",
        ["plan_proposition_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_theme_association_plan_regulation_id"),
        "plan_theme_association",
        ["plan_regulation_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_theme_association_plan_theme_id"),
        "plan_theme_association",
        ["plan_theme_id"],
        unique=False,
        schema="hame",
    )
    op.drop_constraint(
        "plan_theme_id_fkey",
        "plan_proposition",
        schema="hame",
        type_="foreignkey",
    )
    op.drop_column("plan_proposition", "plan_theme_id", schema="hame")
    op.drop_constraint(
        "plan_theme_id_fkey",
        "plan_regulation",
        schema="hame",
        type_="foreignkey",
    )
    op.drop_column("plan_regulation", "plan_theme_id", schema="hame")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan_regulation",
        sa.Column("plan_theme_id", sa.UUID(), autoincrement=False, nullable=True),
        schema="hame",
    )
    op.create_foreign_key(
        "plan_theme_id_fkey",
        "plan_regulation",
        "plan_theme",
        ["plan_theme_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    op.add_column(
        "plan_proposition",
        sa.Column("plan_theme_id", sa.UUID(), autoincrement=False, nullable=True),
        schema="hame",
    )
    op.create_foreign_key(
        "plan_theme_id_fkey",
        "plan_proposition",
        "plan_theme",
        ["plan_theme_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    op.drop_index(
        op.f("ix_hame_plan_theme_association_plan_theme_id"),
        table_name="plan_theme_association",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_plan_theme_association_plan_regulation_id"),
        table_name="plan_theme_association",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_plan_theme_association_plan_proposition_id"),
        table_name="plan_theme_association",
        schema="hame",
    )
    op.drop_table("plan_theme_association", schema="hame")
    # ### end Alembic commands ###
