"""
Note DTO is defined here.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NoteDto:
    """
    Notes Dto used to transfer Note data
    """
    id: int
    title: str
    content: str
    date_created: datetime
