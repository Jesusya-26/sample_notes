"""
Notes endpoints logic of getting entities from the database is defined here.
"""
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, insert, update, delete

from test_fastapi.exceptions.logic.common import EntityNotFoundById, EntityOwnerError
from test_fastapi.db.entities.notes import notes
from test_fastapi.dto import NoteDto, UserDTO
from test_fastapi.schemas import NotePostRequest


class NoteCRUD:
    async def get_all(
            self,
            user: UserDTO,
            session: AsyncConnection
    ) -> list[NoteDto]:
        """
        Get all note objects from crud
        """
        if "admin" in user.roles:
            statement = (select(notes.c.id,
                                notes.c.title,
                                notes.c.content,
                                notes.c.date_created).
                         order_by(notes.c.id))
        else:
            statement = (select(notes.c.id,
                                notes.c.title,
                                notes.c.content,
                                notes.c.date_created).
                         filter(notes.c.user_id == user.id).
                         order_by(notes.c.id))

        return [NoteDto(*data) for data in await session.execute(statement)]

    async def add(
            self,
            user: UserDTO,
            session: AsyncConnection,
            note: NotePostRequest
    ) -> NoteDto:
        """
        Create note object
        """
        statement = insert(notes).values(
            title=note.title,
            content=note.content,
            user_id=user.id
        ).returning(notes.c.id, notes.c.title, notes.c.content, notes.c.date_created)

        result = list(await session.execute(statement))[0]
        await session.commit()

        return NoteDto(*result)

    async def get_by_id(
            self,
            user: UserDTO,
            session: AsyncConnection,
            note_id: int
    ) -> NoteDto:
        """
        Get note by id
        """
        statement = (select(notes).where(notes.c.id == note_id))
        result = (await session.execute(statement)).first()

        if result is None:
            raise EntityNotFoundById(note_id, 'note')
        if result.user_id != user.id and "admin" not in user.roles:
            raise EntityOwnerError(note_id, 'note')

        return NoteDto(*result[:-1])

    async def update_full(
            self,
            user: UserDTO,
            session: AsyncConnection,
            note_id: int,
            data: dict
    ) -> NoteDto:
        """
        Update full note by id
        """

        statement = select(notes).where(notes.c.id == note_id)
        result = (await session.execute(statement)).first()

        if result is None:
            raise EntityNotFoundById(note_id, 'note')
        if result.user_id != user.id and "admin" not in user.roles:
            raise EntityOwnerError(note_id, 'note')

        statement = (update(notes)
                     .values(title=data['title'],
                             content=data['content'])
                     .where(notes.c.id == note_id)
                     .returning(notes.c.id, notes.c.title, notes.c.content, notes.c.date_created))
        result = (await session.execute(statement)).first()

        await session.commit()

        return NoteDto(*result)

    async def update_part(
            self,
            user: UserDTO,
            session: AsyncConnection,
            note_id: int,
            data: dict
    ) -> NoteDto:
        """
        Update part note by id
        """

        statement = select(notes).where(notes.c.id == note_id)
        result = (await session.execute(statement)).first()

        if result is None:
            raise EntityNotFoundById(note_id, 'note')
        if result.user_id != user.id and "admin" not in user.roles:
            raise EntityOwnerError(note_id, 'note')

        statement = (update(notes).
                     where(notes.c.id == note_id).
                     returning(notes.c.id, notes.c.title, notes.c.content, notes.c.date_created))

        if data['title'] is not None:
            statement = statement.values(title=data['title'])
        if data['content'] is not None:
            statement = statement.values(content=data['content'])
        result = (await session.execute(statement)).first()

        await session.commit()

        return NoteDto(*result)

    async def delete(
            self,
            user: UserDTO,
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
        if result.user_id != user.id and "admin" not in user.roles:
            raise EntityOwnerError(note_id, 'note')

        statement = delete(notes).where(notes.c.id == note_id)

        await session.execute(statement)
        await session.commit()
