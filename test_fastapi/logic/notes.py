"""
Notes endpoints logic of getting entities from the database is defined here.
"""
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, insert, update, delete

from test_fastapi.exceptions.logic.common import EntityNotFoundById
from test_fastapi.db.entities.notes import notes
from test_fastapi.dto import NoteDto
from test_fastapi.schemas import NoteRequest


class NoteCRUD:
    async def get_all(
            self,
            session: AsyncConnection
    ) -> list[NoteDto]:
        """
        Get all note objects from crud
        """
        statement = select(notes).order_by(notes.c.id)

        return [NoteDto(*data) for data in await session.execute(statement)]

    async def add(
            self,
            session: AsyncConnection,
            note: NoteRequest
    ) -> NoteDto:
        """
        Create note object
        """
        statement = insert(notes).values(
            title=note.title,
            content=note.content
        ).returning(notes)

        result = list(await session.execute(statement))[0]
        await session.commit()

        return NoteDto(*result)

    async def get_by_id(
            self,
            session: AsyncConnection,
            note_id: int
    ) -> NoteDto:
        """
        Get note by id
        """
        statement = select(notes).where(notes.c.id == note_id)
        result = (await session.execute(statement)).first()
        if result is None:
            raise EntityNotFoundById(note_id, 'note')

        return NoteDto(*result)

    async def update(
            self,
            session: AsyncConnection,
            note_id: int,
            data: dict
    ) -> NoteDto:
        """
        Update note by id
        """

        statement = (update(notes)
                     .values(title=data['title'],
                             content=data['content'])
                     .where(notes.c.id == note_id)
                     .returning(notes))

        result = (await session.execute(statement)).first()
        if result is None:
            raise EntityNotFoundById(note_id, 'note')

        await session.commit()

        return NoteDto(*result)

    async def delete(
            self,
            session: AsyncConnection,
            note_id: int
    ) -> None:
        """
        Delete note by id
        """
        statement = select(notes).where(notes.c.id == note_id)
        result = (await session.execute(statement)).first()
        if result is None:
            raise EntityNotFoundById(note_id, 'note')

        statement = delete(notes).where(notes.c.id == note_id)
        await session.execute(statement)
        await session.commit()
