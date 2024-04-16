"""
Users database table is defined here.
"""
from sqlalchemy import CHAR, Boolean, Column, Table,  text

from sample_notes.db import metadata


users = Table(
    "users",
    metadata,
    Column("id", CHAR(36), primary_key=True),
    Column("is_banned", Boolean, server_default=text("false"), nullable=False),
    schema="users",
)
"""
Columns:
- `id` - user identifier, char 36
- `is_banned` - indicates whether user status is banned, boolean
"""