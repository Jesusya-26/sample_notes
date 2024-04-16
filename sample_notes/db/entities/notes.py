"""
Notes table is defined here.
"""
from sqlalchemy import Table, Column, Integer, String, Text, TIMESTAMP, Identity, func, ForeignKey

from sample_notes.db import metadata

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, server_default=Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1)),
    Column("title", String, nullable=False),
    Column("content", Text, nullable=False),
    Column("date_created", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
    Column("user_id", String, nullable=False)
)

"""
Notes:
- id int 
- title str
- content str
- date_created datetime 
- user_id str
"""
