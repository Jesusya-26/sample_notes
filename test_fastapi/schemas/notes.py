"""
Notes responses and requests are defined here.
"""
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional

from test_fastapi.dto import NoteDto


class NoteResponse(BaseModel):
    """
    Note with all its attributes.
    """

    id: int
    title: str
    content: str
    date_created: datetime

    @classmethod
    def from_dto(cls, dto: NoteDto) -> "NoteResponse":
        """
        Construct from DTO.
        """
        return cls(
            id=dto.id,
            title=dto.title,
            content=dto.content,
            date_created=dto.date_created
        )


class ShortNoteResponse(BaseModel):
    """
    Note with all its attributes.
    """

    id: int
    title: str

    @classmethod
    def from_dto(cls, dto: NoteDto) -> "ShortNoteResponse":
        """
        Construct from DTO.
        """
        return cls(
            id=dto.id,
            title=dto.title
        )


# schema for returning notes
class NotesResponse(BaseModel):
    """
    List of notes.
    """
    notes: list[ShortNoteResponse]

    @classmethod
    def from_dtos(cls, dtos: list[NoteDto]) -> "NotesResponse":
        """
        Construct from DTOs list.
        """
        return cls(notes=[ShortNoteResponse.from_dto(dto) for dto in dtos])


class NotePostRequest(BaseModel):
    """
    Note model for Post request.
    """
    title: str = Field(examples=["Sample title"])
    content: str = Field(examples=["Sample content"])


class NotePatchRequest(BaseModel):
    """
    Note model for Patch request.
    """
    title: Optional[str] = Field(default=None, examples=["Sample title"])
    content: Optional[str] = Field(default=None, examples=["Sample content"])

    @model_validator(mode='before')
    def is_empty_request(cls, values):
        title = values.get('title')
        content = values.get('content')
        if title is None and content is None:
            raise ValueError('request cannot be empty!')
        return values
