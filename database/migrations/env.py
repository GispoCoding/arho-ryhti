import os
from logging.config import fileConfig

from alembic import context
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.replaceable_entity import register_entities
from base import Base

# *ALL* sqlalchemy models have to be imported so that alembic detects all tables
from codes import *  # noqa
from models import *  # noqa
from sqlalchemy import create_engine
from triggers import (  # trgfunc_update_lifecycle_status,; trg_update_lifecycle_status,
    trg_plan_modified_at,
    trgfunc_plan_modified_at,
)

# Register functions and triggers
imported_functions = [
    trgfunc_plan_modified_at,
    trg_plan_modified_at,
    # trgfunc_update_lifecycle_status,
    # trg_update_lifecycle_status,
]

register_entities(entities=imported_functions, entity_types=[PGTrigger, PGFunction])

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Do not check PostGIS extension tables
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name == "spatial_ref_sys":
        return False
    else:
        return True


# Check our schemas
def include_name(name, type_, parent_names):
    if type_ in "schema":
        return name in ["hame", "codes"]
    else:
        return True


# adapted from
# http://allan-simon.github.io/blog/posts/python-alembic-with-environment-variables/
def get_url(connection_params: dict):
    """Allow passing connection params to alembic, or use env values as fallback."""
    user = connection_params.get("user", os.environ.get("SU_USER", "postgres"))
    password = connection_params.get(
        "password", os.environ.get("SU_USER_PW", "postgres")
    )
    host = connection_params.get(
        "host", os.environ.get("DB_INSTANCE_ADDRESS", "localhost")
    )
    port = connection_params.get("port", os.environ.get("DB_INSTANCE_PORT", "5434"))
    dbname = connection_params.get("dbname", os.environ.get("DB_MAIN_NAME", "hame"))
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url({})
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        include_schemas=True,
        include_name=include_name,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    An existing psycopg2 connection cannot be used here.
    We have to provide an sqlalchemy connectable or nothing.
    """
    connection_params = config.attributes.get("connection", {})
    connectable = create_engine(get_url(connection_params))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=True,
            include_name=include_name,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
