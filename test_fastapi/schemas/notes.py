"""
Notes responses and requests are defined here.
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
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


# schema for returning notes
class NotesResponse(BaseModel):
    """
    List of notes.
    """
    notes: list[NoteResponse]

    @classmethod
    def from_dtos(cls, dtos: list[NoteDto]) -> "NotesResponse":
        """
        Construct from DTOs list.
        """
        return cls(notes=[NoteResponse.from_dto(dto) for dto in dtos])


# schema for creating a note
class NoteRequest(BaseModel):
    title: str
    content: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Sample title",
                "content": "Sample content"
            }
        }
    )
