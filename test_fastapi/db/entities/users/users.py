"""
Users database table is defined here.
"""
from sqlalchemy import (CHAR, TIMESTAMP, Boolean, Column, Integer, String,
                        Table, UniqueConstraint, func, text, Identity)

from test_fastapi.db import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, server_default=Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)),
    Column("email", String(64), nullable=False),
    Column("is_approved", Boolean, server_default=text("false"), nullable=False),
    Column("password_hash", CHAR(64), nullable=False),
    Column(
        "registered_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("email", name="users_unique_email"),
    schema="users",
)
"""


Columns:
- `id` - user identifier, int serial
- `email` - user email address, varchar(64)
- `is_approved` - indicates whether user status is approved to update data, boolean
- `password_hash` - user password hashed with salt, varchar(128)
- `registrated_at` - user registration datetime, timestamptz
"""