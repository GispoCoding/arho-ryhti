"""simplify lifecycle triggers

Revision ID: 102e19dd08da
Revises: c9e79d1b4821
Create Date: 2024-11-26 22:00:19.519765

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = "102e19dd08da"
down_revision: Union[str, None] = "c9e79d1b4821"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    hame_plan_regulation_trg_plan_regulation_land_use_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_land_use_area_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_land_use_area_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_regulation_trg_plan_regulation_land_use_area_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_land_use_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_land_use_area_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_land_use_area_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_proposition_trg_plan_proposition_land_use_area_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_land_use_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_land_use_point_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_land_use_point_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_regulation_trg_plan_regulation_land_use_point_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_land_use_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_land_use_point_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_land_use_point_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_proposition_trg_plan_proposition_land_use_point_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_line_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_line_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_line_new_lifecycle_status()",
    )
    op.drop_entity(hame_plan_regulation_trg_plan_regulation_line_new_lifecycle_status)

    hame_plan_proposition_trg_plan_proposition_line_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_line_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_line_new_lifecycle_status()",
    )
    op.drop_entity(hame_plan_proposition_trg_plan_proposition_line_new_lifecycle_status)

    hame_plan_regulation_trg_plan_regulation_other_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_other_area_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_other_area_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_regulation_trg_plan_regulation_other_area_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_other_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_other_area_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_other_area_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_proposition_trg_plan_proposition_other_area_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_other_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_other_point_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_other_point_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_regulation_trg_plan_regulation_other_point_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_other_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_other_point_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_other_point_new_lifecycle_status()",
    )
    op.drop_entity(
        hame_plan_proposition_trg_plan_proposition_other_point_new_lifecycle_status
    )

    hame_trgfunc_plan_regulation_land_use_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_land_use_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_regulation_land_use_area_new_lifecycle_status)

    hame_trgfunc_plan_proposition_land_use_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_land_use_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_proposition_land_use_area_new_lifecycle_status)

    hame_trgfunc_plan_regulation_land_use_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_land_use_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_regulation_land_use_point_new_lifecycle_status)

    hame_trgfunc_plan_proposition_land_use_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_land_use_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_proposition_land_use_point_new_lifecycle_status)

    hame_trgfunc_plan_regulation_line_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_line_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.line\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_regulation_line_new_lifecycle_status)

    hame_trgfunc_plan_proposition_line_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_line_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.line\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_proposition_line_new_lifecycle_status)

    hame_trgfunc_plan_regulation_other_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_other_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_regulation_other_area_new_lifecycle_status)

    hame_trgfunc_plan_proposition_other_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_other_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_proposition_other_area_new_lifecycle_status)

    hame_trgfunc_plan_regulation_other_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_other_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_regulation_other_point_new_lifecycle_status)

    hame_trgfunc_plan_proposition_other_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_other_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.drop_entity(hame_trgfunc_plan_proposition_other_point_new_lifecycle_status)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    hame_trgfunc_plan_proposition_other_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_other_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_proposition_other_point_new_lifecycle_status)

    hame_trgfunc_plan_regulation_other_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_other_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_regulation_other_point_new_lifecycle_status)

    hame_trgfunc_plan_proposition_other_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_other_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_proposition_other_area_new_lifecycle_status)

    hame_trgfunc_plan_regulation_other_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_other_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.other_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_regulation_other_area_new_lifecycle_status)

    hame_trgfunc_plan_proposition_line_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_line_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.line\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_proposition_line_new_lifecycle_status)

    hame_trgfunc_plan_regulation_line_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_line_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.line\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_regulation_line_new_lifecycle_status)

    hame_trgfunc_plan_proposition_land_use_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_land_use_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_proposition_land_use_point_new_lifecycle_status)

    hame_trgfunc_plan_regulation_land_use_point_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_land_use_point_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_point\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_regulation_land_use_point_new_lifecycle_status)

    hame_trgfunc_plan_proposition_land_use_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_land_use_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_proposition_land_use_area_new_lifecycle_status)

    hame_trgfunc_plan_regulation_land_use_area_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_land_use_area_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            DECLARE status_id UUID := (\n                SELECT lifecycle_status_id\n                FROM hame.land_use_area\n                WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n                LIMIT 1\n                );\n            BEGIN\n                IF status_id IS NOT NULL THEN\n                    NEW.lifecycle_status_id = status_id;\n                END IF;\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.create_entity(hame_trgfunc_plan_regulation_land_use_area_new_lifecycle_status)

    hame_plan_proposition_trg_plan_proposition_other_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_other_point_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_other_point_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_proposition_trg_plan_proposition_other_point_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_other_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_other_point_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_other_point_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_regulation_trg_plan_regulation_other_point_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_other_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_other_area_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_other_area_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_proposition_trg_plan_proposition_other_area_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_other_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_other_area_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_other_area_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_regulation_trg_plan_regulation_other_area_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_line_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_line_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_line_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_proposition_trg_plan_proposition_line_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_line_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_line_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_line_new_lifecycle_status()",
    )
    op.create_entity(hame_plan_regulation_trg_plan_regulation_line_new_lifecycle_status)

    hame_plan_proposition_trg_plan_proposition_land_use_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_land_use_point_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_land_use_point_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_proposition_trg_plan_proposition_land_use_point_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_land_use_point_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_land_use_point_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_land_use_point_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_regulation_trg_plan_regulation_land_use_point_new_lifecycle_status
    )

    hame_plan_proposition_trg_plan_proposition_land_use_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_proposition_land_use_area_new_lifecycle_status",
        on_entity="hame.plan_proposition",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_proposition_land_use_area_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_proposition_trg_plan_proposition_land_use_area_new_lifecycle_status
    )

    hame_plan_regulation_trg_plan_regulation_land_use_area_new_lifecycle_status = PGTrigger(
        schema="hame",
        signature="trg_plan_regulation_land_use_area_new_lifecycle_status",
        on_entity="hame.plan_regulation",
        is_constraint=False,
        definition="BEFORE INSERT ON hame.plan_regulation FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_plan_regulation_land_use_area_new_lifecycle_status()",
    )
    op.create_entity(
        hame_plan_regulation_trg_plan_regulation_land_use_area_new_lifecycle_status
    )

    # ### end Alembic commands ###
