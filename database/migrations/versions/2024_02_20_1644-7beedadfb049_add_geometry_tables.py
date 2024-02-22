"""add geometry tables

Revision ID: 7beedadfb049
Revises: 7de05df06dce
Create Date: 2024-02-20 16:44:29.666397

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7beedadfb049"
down_revision: Union[str, None] = "7de05df06dce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "land_use_area",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("source_data_object", sa.String(), nullable=True),
        sa.Column("height_range", postgresql.NUMRANGE(), nullable=True),
        sa.Column("height_unit", sa.String(), nullable=True),
        sa.Column("ordering", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_of_underground_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["plan_id"], ["hame.plan.id"], name="plan_id_fkey"),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_underground_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_area_lifecycle_status_id"),
        "land_use_area",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_area_ordering"),
        "land_use_area",
        ["ordering"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_area_plan_id"),
        "land_use_area",
        ["plan_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_area_plan_regulation_group_id"),
        "land_use_area",
        ["plan_regulation_group_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_area_type_of_underground_id"),
        "land_use_area",
        ["type_of_underground_id"],
        unique=False,
        schema="hame",
    )
    op.create_table(
        "land_use_point",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOINT",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("source_data_object", sa.String(), nullable=True),
        sa.Column("height_range", postgresql.NUMRANGE(), nullable=True),
        sa.Column("height_unit", sa.String(), nullable=True),
        sa.Column("ordering", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_of_underground_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["plan_id"], ["hame.plan.id"], name="plan_id_fkey"),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_underground_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_point_lifecycle_status_id"),
        "land_use_point",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_point_ordering"),
        "land_use_point",
        ["ordering"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_point_plan_id"),
        "land_use_point",
        ["plan_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_point_plan_regulation_group_id"),
        "land_use_point",
        ["plan_regulation_group_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_land_use_point_type_of_underground_id"),
        "land_use_point",
        ["type_of_underground_id"],
        unique=False,
        schema="hame",
    )
    op.create_table(
        "line",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTILINESTRING",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("source_data_object", sa.String(), nullable=True),
        sa.Column("height_range", postgresql.NUMRANGE(), nullable=True),
        sa.Column("height_unit", sa.String(), nullable=True),
        sa.Column("ordering", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_of_underground_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["plan_id"], ["hame.plan.id"], name="plan_id_fkey"),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_underground_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_line_lifecycle_status_id"),
        "line",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_line_ordering"), "line", ["ordering"], unique=False, schema="hame"
    )
    op.create_index(
        op.f("ix_hame_line_plan_id"), "line", ["plan_id"], unique=False, schema="hame"
    )
    op.create_index(
        op.f("ix_hame_line_plan_regulation_group_id"),
        "line",
        ["plan_regulation_group_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_line_type_of_underground_id"),
        "line",
        ["type_of_underground_id"],
        unique=False,
        schema="hame",
    )
    op.create_table(
        "other_area",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("source_data_object", sa.String(), nullable=True),
        sa.Column("height_range", postgresql.NUMRANGE(), nullable=True),
        sa.Column("height_unit", sa.String(), nullable=True),
        sa.Column("ordering", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_of_underground_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["plan_id"], ["hame.plan.id"], name="plan_id_fkey"),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_underground_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_area_lifecycle_status_id"),
        "other_area",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_area_ordering"),
        "other_area",
        ["ordering"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_area_plan_id"),
        "other_area",
        ["plan_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_area_plan_regulation_group_id"),
        "other_area",
        ["plan_regulation_group_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_area_type_of_underground_id"),
        "other_area",
        ["type_of_underground_id"],
        unique=False,
        schema="hame",
    )
    op.create_table(
        "other_point",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOINT",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("source_data_object", sa.String(), nullable=True),
        sa.Column("height_range", postgresql.NUMRANGE(), nullable=True),
        sa.Column("height_unit", sa.String(), nullable=True),
        sa.Column("ordering", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type_of_underground_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("plan_regulation_group_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(["plan_id"], ["hame.plan.id"], name="plan_id_fkey"),
        sa.ForeignKeyConstraint(
            ["plan_regulation_group_id"],
            ["hame.plan_regulation_group.id"],
            name="plan_regulation_group_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["type_of_underground_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_point_lifecycle_status_id"),
        "other_point",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_point_ordering"),
        "other_point",
        ["ordering"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_point_plan_id"),
        "other_point",
        ["plan_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_point_plan_regulation_group_id"),
        "other_point",
        ["plan_regulation_group_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_other_point_type_of_underground_id"),
        "other_point",
        ["type_of_underground_id"],
        unique=False,
        schema="hame",
    )
    op.alter_column(
        "plan",
        "geom",
        existing_type=geoalchemy2.types.Geometry(
            geometry_type="POLYGON",
            srid=3067,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            nullable=False,
            _spatial_index_reflected=True,
        ),
        type_=geoalchemy2.types.Geometry(
            geometry_type="MULTIPOLYGON",
            srid=3067,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            nullable=False,
        ),
        existing_nullable=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_lifecycle_status_id"),
        "plan",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_proposition_lifecycle_status_id"),
        "plan_proposition",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_regulation_lifecycle_status_id"),
        "plan_regulation",
        ["lifecycle_status_id"],
        unique=False,
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_hame_plan_regulation_lifecycle_status_id"),
        table_name="plan_regulation",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_plan_proposition_lifecycle_status_id"),
        table_name="plan_proposition",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_plan_lifecycle_status_id"), table_name="plan", schema="hame"
    )
    op.alter_column(
        "plan",
        "geom",
        existing_type=geoalchemy2.types.Geometry(
            geometry_type="MULTIPOLYGON",
            srid=3067,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            nullable=False,
        ),
        type_=geoalchemy2.types.Geometry(
            geometry_type="POLYGON",
            srid=3067,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            nullable=False,
            _spatial_index_reflected=True,
        ),
        existing_nullable=False,
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_other_point_type_of_underground_id"),
        table_name="other_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_other_point_plan_regulation_group_id"),
        table_name="other_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_other_point_plan_id"), table_name="other_point", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_other_point_ordering"), table_name="other_point", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_other_point_lifecycle_status_id"),
        table_name="other_point",
        schema="hame",
    )
    op.drop_index(
        "idx_other_point_geom",
        table_name="other_point",
        schema="hame",
        postgresql_using="gist",
    )
    op.drop_table("other_point", schema="hame")
    op.drop_index(
        op.f("ix_hame_other_area_type_of_underground_id"),
        table_name="other_area",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_other_area_plan_regulation_group_id"),
        table_name="other_area",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_other_area_plan_id"), table_name="other_area", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_other_area_ordering"), table_name="other_area", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_other_area_lifecycle_status_id"),
        table_name="other_area",
        schema="hame",
    )
    op.drop_index(
        "idx_other_area_geom",
        table_name="other_area",
        schema="hame",
        postgresql_using="gist",
    )
    op.drop_table("other_area", schema="hame")
    op.drop_index(
        op.f("ix_hame_line_type_of_underground_id"), table_name="line", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_line_plan_regulation_group_id"), table_name="line", schema="hame"
    )
    op.drop_index(op.f("ix_hame_line_plan_id"), table_name="line", schema="hame")
    op.drop_index(op.f("ix_hame_line_ordering"), table_name="line", schema="hame")
    op.drop_index(
        op.f("ix_hame_line_lifecycle_status_id"), table_name="line", schema="hame"
    )
    op.drop_index(
        "idx_line_geom", table_name="line", schema="hame", postgresql_using="gist"
    )
    op.drop_table("line", schema="hame")
    op.drop_index(
        op.f("ix_hame_land_use_point_type_of_underground_id"),
        table_name="land_use_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_point_plan_regulation_group_id"),
        table_name="land_use_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_point_plan_id"),
        table_name="land_use_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_point_ordering"),
        table_name="land_use_point",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_point_lifecycle_status_id"),
        table_name="land_use_point",
        schema="hame",
    )
    op.drop_index(
        "idx_land_use_point_geom",
        table_name="land_use_point",
        schema="hame",
        postgresql_using="gist",
    )
    op.drop_table("land_use_point", schema="hame")
    op.drop_index(
        op.f("ix_hame_land_use_area_type_of_underground_id"),
        table_name="land_use_area",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_area_plan_regulation_group_id"),
        table_name="land_use_area",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_area_plan_id"), table_name="land_use_area", schema="hame"
    )
    op.drop_index(
        op.f("ix_hame_land_use_area_ordering"),
        table_name="land_use_area",
        schema="hame",
    )
    op.drop_index(
        op.f("ix_hame_land_use_area_lifecycle_status_id"),
        table_name="land_use_area",
        schema="hame",
    )
    op.drop_index(
        "idx_land_use_area_geom",
        table_name="land_use_area",
        schema="hame",
        postgresql_using="gist",
    )
    op.drop_table("land_use_area", schema="hame")
    # ### end Alembic commands ###
