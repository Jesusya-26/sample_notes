from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, update

from test_fastapi.db.entities import users, notes
from test_fastapi.dto import NoteDto


async def get_all_notes(
        user_id: str,
        session: AsyncConnection
) -> list[NoteDto]:
    """
    Get all note objects from crud
    """

    statement = (select(notes.c.id,
                        notes.c.title,
                        notes.c.content,
                        notes.c.date_created).
                 filter(notes.c.user_id == user_id).
                 order_by(notes.c.id))

    result = (await session.execute(statement)).scalars()

    if result is None:
        raise ValueError('user not found')

    return [NoteDto(*data) for data in result]


async def activate(
        user_id: str,
        session: AsyncConnection
) -> None:
    """
    Activate user by id
    """

    statement = select(users).where(users.c.id == user_id)
    result = (await session.execute(statement)).first()

    if result is None:
        raise ValueError("The user does not exist or has not yet logged in to the service")

    statement = update(users).where(users.c.id == user_id).values(is_banned=False)

    await session.execute(statement)
    await session.commit()


async def deactivate(
        user_id: str,
        session: AsyncConnection
) -> None:
    """
    Block user by id
    """

    statement = select(users).where(users.c.id == user_id)
    result = (await session.execute(statement)).first()

    if result is None:
        raise ValueError("The user does not exist or has not yet logged in to the service")

    statement = update(users).values(is_banned=True).where(users.c.id == user_id)

    await session.execute(statement)
    await session.commit()
