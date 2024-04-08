from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from test_fastapi.db.connection import get_connection
from test_fastapi.logic.admin import get_all_notes, activate, deactivate
from test_fastapi.schemas import NotesResponse
from test_fastapi.dto.users import UserDTO
from test_fastapi.utils.dependencies import user_dependency


from .router import admin_data_router


@admin_data_router.get(
    "/notes",
    response_model=NotesResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_notes(
    user_id: str,
    session: AsyncConnection = Depends(get_connection),
    user: UserDTO = Depends(user_dependency)
) -> NotesResponse:
    """
    API endpoint for listing all note resources of user with given id

    Args:
        user_id: string
    """

    if 'admin' not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")

    notes = await get_all_notes(user_id, session)
    return NotesResponse.from_dtos(notes)


@admin_data_router.post(
    "/activate",
    status_code=status.HTTP_200_OK,
)
async def activate_user(
        user_id: str,
        session: AsyncConnection = Depends(get_connection),
        user: UserDTO = Depends(user_dependency)
) -> dict:
    """API endpoint for activate user with given id

    Args:
        user_id: string
    """

    if 'admin' not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")

    try:
        await activate(user_id, session)
        return {"result": f"User with id={user_id} is active"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))


@admin_data_router.post(
    "/deactivate",
    status_code=status.HTTP_200_OK,
)
async def deactivate_user(
        user_id: str,
        session: AsyncConnection = Depends(get_connection),
        user: UserDTO = Depends(user_dependency)
) -> dict:
    """API endpoint for activate user with given id

    Args:
        user_id: string
    """

    if 'admin' not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")

    try:
        await deactivate(user_id, session)
        return {"result": f"User with id={user_id} was blocked"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
