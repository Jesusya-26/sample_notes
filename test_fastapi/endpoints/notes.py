"""
get_all_note, create_note, get_note_by_id, update_note, delete_note endpoints are defined here.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from test_fastapi.db.connection import get_connection
from test_fastapi.logic import NoteCRUD
from test_fastapi.schemas import NoteResponse, NotesResponse, NotePostRequest, NotePatchRequest
from test_fastapi.dto.users import User
from test_fastapi.utils.dependencies import get_user_info as user_dependency


from .routers import notes_router

crud = NoteCRUD()


@notes_router.get(
    "/",
    response_model=NotesResponse,
    status_code=status.HTTP_200_OK
)
async def get_all_notes(
    session: AsyncConnection = Depends(get_connection),
    user: User = Depends(user_dependency)
) -> NotesResponse:
    """
    API endpoint for listing all note resources
    """
    notes = await crud.get_all(user.id, session)

    return NotesResponse.from_dtos(notes)


@notes_router.post(
    "/",

    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
        note_data: NotePostRequest,
        session: AsyncConnection = Depends(get_connection),
        user: User = Depends(user_dependency)
) -> NoteResponse:
    """API endpoint for creating a note resource

    Args:
        note_data (NotePostRequest): crud for creating a note using the note schema

    Returns:
        NoteResponse: note that has been created
    """

    note = await crud.add(user.id, session, note_data)

    return NoteResponse.from_dto(note)


@notes_router.get(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
)
async def get_note_by_id(
        note_id: int,
        session: AsyncConnection = Depends(get_connection),
        user: User = Depends(user_dependency)
) -> NoteResponse:
    """API endpoint for retrieving a note by its ID

    Args:
        note_id (str): the ID of the note to retrieve

    Returns:
        NoteResponse: The retrieved note
    """
    note = await crud.get_by_id(user.id, session, note_id)

    return NoteResponse.from_dto(note)


@notes_router.put(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK
)
async def update_full_note(
        note_id: int,
        data: NotePostRequest,
        session: AsyncConnection = Depends(get_connection),
        user: User = Depends(user_dependency)
) -> NoteResponse:
    """Update full note by ID

    Args:
        note_id (str): ID of note to update
        data (NotePostRequest): crud to update note

    Returns:
        dict: the updated note
    """
    note = await crud.update_full(user.id, session, note_id, data={"title": data.title,
                                                                   "content": data.content})

    return NoteResponse.from_dto(note)


@notes_router.patch(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK
)
async def update_part_note(
        note_id: int,
        data: NotePatchRequest,
        session: AsyncConnection = Depends(get_connection),
        user: User = Depends(user_dependency)
) -> NoteResponse:
    """Update the title or content (or both) by ID

    Args:
        note_id (str): ID of note to update
        data (NotePostRequest): crud to update note

    Returns:
        dict: the updated note
    """
    note = await crud.update_part(user.id, session, note_id, data={"title": data.title,
                                                                   "content": data.content})

    return NoteResponse.from_dto(note)


@notes_router.delete(
    "/{note_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_note(
        note_id: int,
        session: AsyncConnection = Depends(get_connection),
        user: User = Depends(user_dependency)
) -> dict:
    """Delete note by id

    Args:
        note_id (str): ID of note to delete

    """

    await crud.delete(user.id, session, note_id)

    return {"result": "deleted"}
