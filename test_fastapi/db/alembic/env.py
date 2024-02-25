"""
Environment preparation for Alembic.
"""
import os
import pathlib
import sys


project_dir = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_dir))
from test_fastapi.utils.dotenv import try_load_envfile


try_load_envfile(os.environ.get("ENVFILE", str(project_dir / ".env")))


import asyncpg
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from test_fastapi.config.app_settings_global import AppSettings, app_settings
from test_fastapi.db import DeclarativeBase
from test_fastapi.db.entities import *


config = context.config
section = config.config_ini_section

app_settings.update(AppSettings.try_from_env())

config.set_section_option(section, "POSTGRES_DB", app_settings.db_name)
config.set_section_option(section, "POSTGRES_HOST", app_settings.db_addr)
config.set_section_option(section, "POSTGRES_USER", app_settings.db_user)
config.set_section_option(section, "POSTGRES_PASSWORD", app_settings.db_pass)
config.set_section_option(section, "POSTGRES_PORT", str(app_settings.db_port))


fileConfig(config.config_file_name, disable_existing_loggers=False)
target_metadata = DeclarativeBase.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()