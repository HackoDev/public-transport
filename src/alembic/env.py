from __future__ import with_statement
import os
import sys

sys.path.append(os.path.join(os.getcwd()))
from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

from models import metadata

target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


exclude_tables = config.get_section(
    'alembic:exclude'
).get('tables', '').split(',')


def include_object(object, name, type_, reflected, compare_to):
    """ Hook for excluding PostGis tables """
    if type_ == "table" and name in exclude_tables:
        return False
    else:
        return True


def get_url():
    return 'postgres://%s:%s@%s/%s' % (
        os.getenv('POSTGRES_USER', 'postgres'),
        os.getenv('POSTGRES_PASSWORD', ''),
        os.getenv('POSTGRES_HOST', 'localhost'),
        os.getenv('POSTGRES_DB', 'test_db'),
    )


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
