from textwrap import dedent

from alembic_utils.pg_function import PGFunction

regulation_values = PGFunction(
    schema="hame",
    signature="regulation_values(table_name text, id uuid)",
    definition=dedent(
        """\
        RETURNS jsonb
        LANGUAGE plpgsql
        COST 100
        STABLE
        PARALLEL SAFE
        AS $BODY$
        DECLARE
            return_value jsonb;
        BEGIN
            EXECUTE format(
                $SQL$
                WITH additional_info_grouped_by_type AS (
                    SELECT
                        r.id AS regulation_id,
                        tpr.value AS regulation_type,
                        jsonb_agg(
                            jsonb_strip_nulls(
                                jsonb_build_object(
                                    'numeric_value', r.numeric_value,
                                    'unit', r.unit,
                                    'numeric_range_min', r.numeric_range_min,
                                    'numeric_range_max', r.numeric_range_max,
                                    'text_value', r.text_value,
                                    'text_syntax', r.text_syntax,
                                    'code_title', r.code_title,
                                    'code_list', r.code_list,
                                    'code_value', r.code_value
                                )
                            )
                        ) AS additional_info_array
                    FROM hame.regulation_group_association rga
                    JOIN hame.plan_regulation_group rg
                        ON rga.plan_regulation_group_id = rg.id
                    JOIN hame.plan_regulation r
                        ON rg.id = r.plan_regulation_group_id
                    JOIN codes.type_of_plan_regulation tpr
                        ON r.type_of_plan_regulation_id = tpr.id
                    WHERE rga.%I = $1
                      AND r.value_data_type IS NOT NULL
                    GROUP BY r.id, tpr.value
                )
                SELECT
                    jsonb_object_agg(regulation_type, additional_info_array)
                FROM additional_info_grouped_by_type
                $SQL$,
                table_name || '_id'
            )
            INTO return_value
            USING id;

            RETURN return_value;
        END;
        $BODY$;
        """
    ),
)

primary_use_regulations = PGFunction(
    schema="hame",
    signature="primary_use_regulations(land_use_area_id uuid)",
    definition=dedent(
        """\
        RETURNS jsonb
        STABLE
        PARALLEL SAFE
        LANGUAGE sql
        AS
        $$
        WITH additional_info_grouped_by_type AS (
            SELECT
                r.id AS regulation_id,
                tai.value AS type_name,
                jsonb_agg(
                    jsonb_strip_nulls(
                        jsonb_build_object(
                            'numeric_value', ai.numeric_value,
                            'unit', ai.unit,
                            'numeric_range_min', ai.numeric_range_min,
                            'numeric_range_max', ai.numeric_range_max,
                            'text_value', ai.text_value,
                            'text_syntax', ai.text_syntax,
                            'code_title', ai.code_title,
                            'code_list', ai.code_list,
                            'code_value', ai.code_value
                        )
                    )
                ) AS additional_info_array
            FROM hame.additional_information ai
            JOIN codes.type_of_additional_information tai
                ON ai.type_additional_information_id = tai.id
            JOIN hame.plan_regulation r
                ON ai.plan_regulation_id = r.id
            WHERE tai.value != 'paakayttotarkoitus'
            GROUP BY r.id, tai.value
        ),
        additional_info_per_regulation AS (
            SELECT
                regulation_id,
                jsonb_object_agg(type_name, additional_info_array) AS additional_info_json
            FROM additional_info_grouped_by_type
            GROUP BY regulation_id
        )
        SELECT
            jsonb_object_agg(
                tpr.value,
                coalesce(additional_info_per_regulation.additional_info_json, '{}'::jsonb)
            )
        FROM hame.regulation_group_association rga
        JOIN hame.plan_regulation_group rg
            ON rga.plan_regulation_group_id = rg.id
        JOIN hame.plan_regulation r
            ON rg.id = r.plan_regulation_group_id
        JOIN codes.type_of_plan_regulation tpr
            ON r.type_of_plan_regulation_id = tpr.id
        LEFT JOIN additional_info_per_regulation
            ON r.id = additional_info_per_regulation.regulation_id
        WHERE rga.land_use_area_id = $1
          AND EXISTS (
              SELECT 1
              FROM hame.additional_information ai
              JOIN codes.type_of_additional_information tai
                  ON ai.type_additional_information_id = tai.id
              WHERE ai.plan_regulation_id = r.id
                AND tai.value = 'paakayttotarkoitus'
          );
        $$;
        """
    ),
)


sub_area_regulations = PGFunction(
    schema="hame",
    signature="sub_area_regulations(other_area_id uuid)",
    definition=dedent(
        """\
        RETURNS jsonb
        STABLE
        PARALLEL SAFE
        LANGUAGE sql
        AS
        $$
        WITH additional_info_grouped_by_type AS (
            SELECT
                r.id AS regulation_id,
                tai.value AS type_name,
                jsonb_agg(
                    jsonb_strip_nulls(
                        jsonb_build_object(
                            'numeric_value', ai.numeric_value,
                            'unit', ai.unit,
                            'numeric_range_min', ai.numeric_range_min,
                            'numeric_range_max', ai.numeric_range_max,
                            'text_value', ai.text_value,
                            'text_syntax', ai.text_syntax,
                            'code_title', ai.code_title,
                            'code_list', ai.code_list,
                            'code_value', ai.code_value
                        )
                    )
                ) AS additional_info_array
            FROM hame.additional_information ai
            JOIN codes.type_of_additional_information tai
                ON ai.type_additional_information_id = tai.id
            JOIN hame.plan_regulation r
                ON ai.plan_regulation_id = r.id
            WHERE tai.value != 'osaAlue'
            GROUP BY r.id, tai.value
        ),
        additional_info_per_regulation AS (
            SELECT
                regulation_id,
                jsonb_object_agg(type_name, additional_info_array) AS additional_info_json
            FROM additional_info_grouped_by_type
            GROUP BY regulation_id
        )
        SELECT
            jsonb_object_agg(
                tpr.value,
                coalesce(additional_info_per_regulation.additional_info_json, '{}'::jsonb)
            )
        FROM hame.regulation_group_association rga
        JOIN hame.plan_regulation_group rg
            ON rga.plan_regulation_group_id = rg.id
        JOIN hame.plan_regulation r
            ON rg.id = r.plan_regulation_group_id
        JOIN codes.type_of_plan_regulation tpr
            ON r.type_of_plan_regulation_id = tpr.id
        LEFT JOIN additional_info_per_regulation
            ON r.id = additional_info_per_regulation.regulation_id
        WHERE rga.other_area_id = $1
          AND EXISTS (
              SELECT 1
              FROM hame.additional_information ai
              JOIN codes.type_of_additional_information tai
                  ON ai.type_additional_information_id = tai.id
              WHERE ai.plan_regulation_id = r.id
                AND tai.value = 'osaAlue'
          );
        $$;
        """
    ),
)


short_names = PGFunction(
    schema="hame",
    signature="short_names(table_name text, id uuid)",
    definition=dedent(
        """\
            RETURNS text[]
            STABLE
            PARALLEL SAFE
            LANGUAGE plpgsql
        AS
        $BODY$
        DECLARE
            return_value text[];
        BEGIN
            EXECUTE format(
                $SQL$
                SELECT array(
                    SELECT rg.short_name
                    FROM
                        hame.regulation_group_association rga
                        join hame.plan_regulation_group rg
                            on rga.plan_regulation_group_id = rg.id
                    WHERE
                        rga.%I = $1
                        AND rg.short_name is not null
                )
                $SQL$,
                table_name||'_id'
            )
            INTO return_value
            USING id;

            RETURN return_value;
        END;
        $BODY$
        ;
        """
    ),
)

type_regulations = PGFunction(
    schema="hame",
    signature="type_regulations(table_name text, id uuid)",
    definition=dedent(
        """\
        RETURNS jsonb
        STABLE
        PARALLEL SAFE
        LANGUAGE plpgsql
        AS
        $BODY$
        DECLARE
            return_value jsonb;
        BEGIN
            EXECUTE format(
                $SQL$
                WITH additional_info_grouped_by_type AS (
                    SELECT
                        r.id AS regulation_id,
                        tai.value AS type_name,
                        jsonb_agg(
                            jsonb_strip_nulls(
                                jsonb_build_object(
                                    'numeric_value', ai.numeric_value,
                                    'unit', ai.unit,
                                    'numeric_range_min', ai.numeric_range_min,
                                    'numeric_range_max', ai.numeric_range_max,
                                    'text_value', ai.text_value,
                                    'text_syntax', ai.text_syntax,
                                    'code_title', ai.code_title,
                                    'code_list', ai.code_list,
                                    'code_value', ai.code_value
                                )
                            )
                        ) AS additional_info_array
                    FROM hame.additional_information ai
                    JOIN codes.type_of_additional_information tai
                        ON ai.type_additional_information_id = tai.id
                    JOIN hame.plan_regulation r
                        ON ai.plan_regulation_id = r.id
                    GROUP BY r.id, tai.value
                ),
                additional_info_per_regulation AS (
                    SELECT
                        regulation_id,
                        jsonb_object_agg(type_name, additional_info_array) AS additional_info_json
                    FROM additional_info_grouped_by_type
                    GROUP BY regulation_id
                )
                SELECT
                    jsonb_object_agg(
                        tpr.value,
                        coalesce(additional_info_per_regulation.additional_info_json, '{}'::jsonb)
                    )
                FROM hame.regulation_group_association rga
                JOIN hame.plan_regulation_group rg
                    ON rga.plan_regulation_group_id = rg.id
                JOIN hame.plan_regulation r
                    ON rg.id = r.plan_regulation_group_id
                JOIN codes.type_of_plan_regulation tpr
                    ON r.type_of_plan_regulation_id = tpr.id
                LEFT JOIN additional_info_per_regulation
                    ON r.id = additional_info_per_regulation.regulation_id
                WHERE rga.%I = $1
                  AND r.value_data_type IS NULL
                $SQL$,
                table_name||'_id'
            )
            INTO return_value
            USING id;

            RETURN return_value;
        END;
        $BODY$;
        """
    ),
)


functions = [
    regulation_values,
    primary_use_regulations,
    sub_area_regulations,
    type_regulations,
    short_names,
]
