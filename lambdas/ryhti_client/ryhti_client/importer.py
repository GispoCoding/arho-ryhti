from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from database.enums import AttributeValueDataType

load_dotenv(str(Path(__file__).parent.parent.parent.parent / ".env"))
from functools import cache
from typing import TYPE_CHECKING, Any, Optional, cast
from uuid import UUID

from geoalchemy2.shape import from_shape
from pydantic import ValidationError
from ryhti_api_client import AdditionalInformation as RyhtiAdditionalInformation
from ryhti_api_client import AttributeValue as RyhtiAttributeValue
from ryhti_api_client import GeneralRegulationGroup as RyhtiGeneralRegulationGroup
from ryhti_api_client import LanguageString as RyhtiLanguageString
from ryhti_api_client import Plan as RyhtiPlan
from ryhti_api_client import PlanObject as RyhtiPlanObject
from ryhti_api_client import PlanRecommendation as RyhtiPlanRecommendation
from ryhti_api_client import PlanRegulation as RyhtiPlanRegulation
from ryhti_api_client import PlanRegulationGroup as RyhtiPlanRegulationGroup
from ryhti_api_client import RyhtiGeometry
from shapely import (
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    from_geojson,
)
from shapely.geometry.base import BaseGeometry
from sqlalchemy import create_engine, exists, select
from sqlalchemy.orm import Session

from database.base import PROJECT_SRID
from database.codes import AdministrativeRegion, CodeBase, Municipality
from database.db_helper import DatabaseHelper, User
from database.models import (
    AdditionalInformation,
    LandUseArea,
    LandUsePoint,
    Line,
    Organisation,
    OtherArea,
    OtherPoint,
    Plan,
    PlanObjectBase,
    PlanProposition,
    PlanRegulation,
    PlanRegulationGroup,
)

if TYPE_CHECKING:
    from uuid import UUID

    from geoalchemy2.elements import WKBElement


class PlanMatterData(BaseModel):
    name: str
    plan_type_id: UUID
    organization_id: UUID
    permanent_plan_identifier: Optional[str] = None
    producers_plan_identifier: Optional[str] = None


def plan_matter_data_from_json(json_data: str) -> PlanMatterData:
    try:
        plan_matter_data = PlanMatterData.model_validate_json(json_data)
    except ValidationError as e:
        raise ValueError(f"Invalid extra data: \n{e}") from e
    return plan_matter_data


def ryhti_plan_from_json(json_data: str) -> RyhtiPlan:
    try:
        ryhti_plan = RyhtiPlan.model_validate_json(json_data)
    except ValidationError as e:
        raise ValueError(f"Invalid plan data: \n{e}") from e
    return ryhti_plan


class Importer:
    def __init__(self, session: Session):
        self.session = session

    def _get_model_and_code(self, code_uri: str) -> tuple[type[CodeBase], str]:
        CodeModel = next(
            (
                model
                for model in CodeBase.__subclasses__()
                if model.code_list_uri and code_uri.startswith(model.code_list_uri)
            ),
            None,
        )
        if CodeModel is None:
            raise ValueError(f"No matching code list found for URI: {code_uri}")

        code = (
            code_uri.removeprefix(CodeModel.code_list_uri)
            .removeprefix("/")
            .removeprefix("code/")
        )

        return (CodeModel, code)

    @cache
    def get_code_id(self, code_uri: str) -> Optional["UUID"]:
        if not code_uri:
            return None

        CodeModel, code = self._get_model_and_code(code_uri)
        code_uuid = self.session.scalars(
            select(CodeModel.id).where(CodeModel.value == code)
        ).one_or_none()

        return code_uuid

    @cache
    def get_code_instance(self, code_uri: str) -> Optional[CodeBase]:
        if not code_uri:
            return None

        CodeModel, code = self._get_model_and_code(code_uri)
        code_instance = self.session.scalars(
            select(CodeModel).where(CodeModel.value == code)
        ).one_or_none()

        return code_instance

    def deserialize_ryhti_geometry(self, geometry: RyhtiGeometry) -> "WKBElement":
        if int(geometry.srid) != PROJECT_SRID:
            raise ValueError(
                f"Unsupported SRID: {geometry.srid}, expected: {PROJECT_SRID}"
            )
        json = geometry.geometry.model_dump_json()
        shape = from_geojson(json)

        multi_shape = self.convert_to_multi_geom(shape)
        return from_shape(multi_shape, srid=int(geometry.srid))

    def convert_to_multi_geom(
        self, shape: BaseGeometry
    ) -> MultiPolygon | MultiPoint | MultiLineString | BaseGeometry:
        if shape.geom_type == "Polygon":
            shape = MultiPolygon([cast(Polygon, shape)])
        elif shape.geom_type == "Point":
            shape = MultiPoint([cast(Point, shape)])
        elif shape.geom_type == "LineString":
            shape = MultiLineString([cast(LineString, shape)])

        return shape

    def deserialize_language_string(
        self, ryhti_language_string: RyhtiLanguageString
    ) -> dict[str, str] | None:
        languages = ["fin", "swe", "smn", "sms", "sme", "eng"]
        return {
            lang: text
            for lang in languages
            if (text := getattr(ryhti_language_string, lang, None))
        } or None

    def form_value_dict(self, value: RyhtiAttributeValue | None) -> dict[str, Any]:
        if value is None:
            return {}

        data_type = AttributeValueDataType(value.data_type)
        if data_type is AttributeValueDataType.CODE:
            database_field_values = {
                "code_value": value.code,
                "code_list": value.code_list,
                "code_title": self.deserialize_language_string(value.title),
            }
        elif data_type in (
            AttributeValueDataType.NUMERIC,
            AttributeValueDataType.POSITIVE_NUMERIC,
            AttributeValueDataType.DECIMAL,
            AttributeValueDataType.POSITIVE_DECIMAL,
            AttributeValueDataType.SPOT_ELEVATION,
        ):
            database_field_values = {
                "numeric_value": value.number,
                "unit": value.unit_of_measure,
            }
        elif data_type in (
            AttributeValueDataType.NUMERIC_RANGE,
            AttributeValueDataType.POSITIVE_NUMERIC_RANGE,
            AttributeValueDataType.DECIMAL_RANGE,
            AttributeValueDataType.POSITIVE_DECIMAL_RANGE,
        ):
            database_field_values = {
                "numeric_range_min": value.minimum_value,
                "numeric_range_max": value.maximum_value,
                "unit": value.unit_of_measure,
            }
        elif data_type is AttributeValueDataType.IDENTIFIER:
            pass  # TODO implement identifier values
        elif data_type in (
            AttributeValueDataType.LOCALIZED_TEXT,
            AttributeValueDataType.TEXT,
        ):
            database_field_values = {
                "text_value": self.deserialize_language_string(value.text),
                "text_syntax": value.syntax,
            }

        elif data_type in (
            AttributeValueDataType.TIME_PERIOD,
            AttributeValueDataType.TIME_PERIOD_DATE_ONLY,
        ):
            pass  # TODO: implement time period and time period date only values
        else:
            database_field_values = {}

        database_field_values["value_data_type"] = value.data_type
        return database_field_values

    def deserialize_additional_information(
        self, additional_information: RyhtiAdditionalInformation
    ) -> AdditionalInformation:
        value = self.form_value_dict(additional_information.value)
        return AdditionalInformation(
            type_additional_information_id=self.get_code_id(
                additional_information.type
            ),
            **value,
        )

    def deserialize_regulation(
        self, ryhti_regulation: RyhtiPlanRegulation
    ) -> PlanRegulation:
        value = self.form_value_dict(ryhti_regulation.value)

        return PlanRegulation(
            id=ryhti_regulation.plan_regulation_key,
            type_of_plan_regulation_id=self.get_code_id(ryhti_regulation.type),
            lifecycle_status_id=self.get_code_id(ryhti_regulation.life_cycle_status),
            additional_information=[
                self.deserialize_additional_information(a_i)
                for a_i in ryhti_regulation.additional_informations
            ],
            **value,
        )

    def deserialize_recommendation(
        self, ryhti_plan_recommendation: RyhtiPlanRecommendation
    ) -> PlanProposition:
        return PlanProposition(
            id=ryhti_plan_recommendation.plan_recommendation_key,
            lifecycle_status_id=self.get_code_id(
                ryhti_plan_recommendation.life_cycle_status
            ),
            ordering=ryhti_plan_recommendation.recommendation_number,
            plan_themes=[
                self.get_code_id(theme_code)
                for theme_code in ryhti_plan_recommendation.plan_themes
            ],
            text_value=self.deserialize_language_string(
                ryhti_plan_recommendation.value
            ),
        )

    def deserialize_plan_regulation_group(
        self, regulation_group: RyhtiPlanRegulationGroup
    ):
        return PlanRegulationGroup(
            id=regulation_group.plan_regulation_group_key,
            name=self.deserialize_language_string(
                regulation_group.title_of_plan_regulation
            ),
            short_name=regulation_group.letter_identifier,
            ordering=regulation_group.group_number,
            plan_regulations=[
                self.deserialize_regulation(regulation)
                for regulation in regulation_group.plan_regulations
            ],
            plan_propositions=[],
        )

    def deserialize_general_regulation_group(
        self, ryhti_general_regulation_group: RyhtiGeneralRegulationGroup
    ) -> PlanRegulationGroup:
        return PlanRegulationGroup(
            id=ryhti_general_regulation_group.general_regulation_group_key,
            name=self.deserialize_language_string(
                ryhti_general_regulation_group.title_of_plan_regulation
            ),
            ordering=ryhti_general_regulation_group.group_number,
            plan_regulations=[
                self.deserialize_regulation(regulation)
                for regulation in ryhti_general_regulation_group.plan_regulations
            ],
        )

    def deserialize_plan_object(
        self, ryhti_plan_object: RyhtiPlanObject
    ) -> LandUseArea | OtherArea | LandUsePoint | OtherPoint | Line:
        shape = from_geojson(ryhti_plan_object.geometry.geometry.model_dump_json())
        shape = self.convert_to_multi_geom(shape)
        PlanObjectClass: (
            type[LandUseArea]
            | type[OtherArea]
            | type[LandUsePoint]
            | type[OtherPoint]
            | type[Line]
            | None
        ) = None
        if shape.geom_type == "MultiPolygon":
            PlanObjectClass = LandUseArea
        elif shape.geom_type == "MultiPoint":
            PlanObjectClass = LandUsePoint
        elif shape.geom_type == "MultiLineString":
            PlanObjectClass = Line

        if PlanObjectClass is None:
            raise ValueError()

        plan_object = PlanObjectClass(
            id=ryhti_plan_object.plan_object_key,
            name=self.deserialize_language_string(ryhti_plan_object.name),
            description=self.deserialize_language_string(ryhti_plan_object.description),
            lifecycle_status_id=self.get_code_id(ryhti_plan_object.life_cycle_status),
            type_of_underground_id=self.get_code_id(
                ryhti_plan_object.underground_status
            ),
            geom=from_shape(shape),
            ordering=ryhti_plan_object.object_number,
            height_min=(
                ryhti_plan_object.vertical_limit.minimum_value
                if ryhti_plan_object.vertical_limit
                else None
            ),
            height_max=(
                ryhti_plan_object.vertical_limit.maximum_value
                if ryhti_plan_object.vertical_limit
                else None
            ),
            height_unit=(
                ryhti_plan_object.vertical_limit.unit_of_measure
                if ryhti_plan_object.vertical_limit
                else None
            ),
        )
        return plan_object

    def deserialise_ryhti_plan(self, ryhti_plan: RyhtiPlan) -> Plan:
        """Deserializes a RyhtiPlan into a Plan SQLAlchemy model instance."""

        plan_regulation_groups = {
            regulation_group.id: regulation_group
            for ryhti_group in ryhti_plan.plan_regulation_groups
            if (regulation_group := self.deserialize_plan_regulation_group(ryhti_group))
        }

        general_regulation_groups = [
            self.deserialize_general_regulation_group(ryhti_group)
            for ryhti_group in ryhti_plan.general_regulation_groups
        ]

        plan_objects = {
            plan_object.id: plan_object
            for ryhti_plan_object in ryhti_plan.plan_objects
            if (plan_object := self.deserialize_plan_object(ryhti_plan_object))
        }

        for regulation_group_relation in ryhti_plan.plan_regulation_group_relations:
            plan_objects[
                regulation_group_relation.plan_object_key
            ].plan_regulation_groups.append(
                plan_regulation_groups[
                    regulation_group_relation.plan_regulation_group_key
                ]
            )

        plan = Plan(
            id=UUID(ryhti_plan.plan_key),
            # organisation # not included in plan, part of plan matter
            # plan_type # not included in plan, part of plan matter
            # permanent_plan_identifier # not included in plan, part of plan matter
            # producers_plan_identifier # not included in plan, part of plan matter
            # name # not included in plan, part of plan matter
            description=self.deserialize_language_string(ryhti_plan.plan_description),
            scale=ryhti_plan.scale,
            lifecycle_status_id=self.get_code_id(ryhti_plan.life_cycle_status),
            geom=self.deserialize_ryhti_geometry(ryhti_plan.geographical_area),
            legal_effects_of_master_plan=[
                code
                for effect in ryhti_plan.legal_effect_of_local_master_plans
                if (code := self.get_code_instance(effect)) is not None
            ],
            regulation_groups=list(plan_regulation_groups.values())
            + general_regulation_groups,
            general_plan_regulation_groups=general_regulation_groups,
            land_use_areas=[
                p_o for p_o in plan_objects.values() if isinstance(p_o, LandUseArea)
            ],
            other_areas=[
                p_o for p_o in plan_objects.values() if isinstance(p_o, OtherArea)
            ],
            land_use_points=[
                p_o for p_o in plan_objects.values() if isinstance(p_o, LandUsePoint)
            ],
            other_points=[
                p_o for p_o in plan_objects.values() if isinstance(p_o, OtherPoint)
            ],
            lines=[p_o for p_o in plan_objects.values() if isinstance(p_o, Line)],
        )

        plan = self._populate_plan_matter_data_to_plan(plan, plan_matter_data)
        plan = self._determine_and_update_regulation_group_types(plan)

        return plan

    def _populate_plan_matter_data_to_plan(
        self, plan: Plan, plan_matter_data: PlanMatterData
    ) -> Plan:
        plan_type_id = plan_matter_data.plan_type_id
        if not plan_type_id:
            raise ValueError()
        plan.plan_type_id = plan_type_id
        plan.name = {"fin": plan_matter_data.name}
        plan.permanent_plan_identifier = plan_matter_data.permanent_plan_identifier
        plan.producers_plan_identifier = plan_matter_data.producers_plan_identifier
        plan.organisation_id = plan_matter_data.organization_id

        return plan

    def _determine_and_update_regulation_group_types(self, plan: Plan):
        for group in plan.regulation_groups:
            group.type_of_plan_regulation_group_id = UUID(
                "81c44273-6729-4728-9e2f-240b3bb30332"
            )

        for group in plan.general_plan_regulation_groups:
            group.type_of_plan_regulation_group_id = UUID(
                "2204a9f1-04a7-4e1b-b1dd-7d60a512a6ff"
            )

        return plan

    def import_plan(
        self,
        ryhti_plan: RyhtiPlan,
        plan_matter_data: PlanMatterData,
        force: bool = False,
    ) -> bool:
        plan = importer.deserialise_ryhti_plan(ryhti_plan)
        existing_plan = self.session.get(Plan, plan.id)
        if existing_plan:
            if force is True:
                self.session.delete(existing_plan)
                self.session.flush()
            else:
                raise Exception("Plan already exists. Use force to replace the plan.")

        self.session.add(plan)
        self.session.commit()

        return True


if __name__ == "__main__":
    plan_data = Path(
        "/home/lkajan/projects/arho-ryhti/ryhti_debug/e4b2bcf3-0c7f-4e38-90d9-02fc9c4ea82c.json"
    ).read_text()
    ryhti_plan = ryhti_plan_from_json(plan_data)
    plan_matter_data = PlanMatterData(
        name="Importoitu kaava 1",
        organization_id=UUID("cfc10ed7-cbc2-4303-b8d4-e360d3eb3d17"),
        plan_type_id=UUID("0b730644-bfa3-463f-a768-82bae01f6dd5"),
    )
    db_helper = DatabaseHelper(user=User.READ_WRITE)
    connection_string = db_helper.get_connection_string()
    engine = create_engine(connection_string)
    with Session(engine, autoflush=False) as session:
        importer = Importer(session)
        importer.import_plan(ryhti_plan, plan_matter_data, force=True)
