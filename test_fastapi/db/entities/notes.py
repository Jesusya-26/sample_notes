"""
Notes table is defined here.
"""
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Identity
from datetime import datetime

from test_fastapi.db import metadata


# the database model for notes
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, server_default=Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)),
    Column("title", String, nullable=False),
    Column("content", Text, nullable=False),
    Column("date_created", DateTime, default=datetime.utcnow())
)

"""
Notes:
    id int
    title str
    content str
    date_created datetime
"""