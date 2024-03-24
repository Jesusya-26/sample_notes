"""
FastApi dependencies are defined here.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncConnection

from test_fastapi.db.connection import get_connection
from test_fastapi.dto.users import User as UserDTO
from test_fastapi.exceptions.logic.users import AccessTokenExpiredError
from test_fastapi.logic.users import get_user_info, validate_user_token
from test_fastapi.utils.tokens import Token


def access_token_dependency(access_token: OAuth2PasswordBearer(tokenUrl="/api/login") = Depends()) -> Token:
    """
    Return token constructed from JWT token given in `Authorization` header.
    """
    return Token.from_jwt(access_token)


async def user_dependency(
    access_token: Token = Depends(access_token_dependency),
    conn: AsyncConnection = Depends(get_connection),
) -> UserDTO:
    """
    Return user fetched from the database by email from a validated access token.

    Ensures that User is approved to log in and valid.
    """
    if not await validate_user_token(conn, access_token):
        raise AccessTokenExpiredError(access_token)
    return await get_user_info(conn, access_token.email, access_token.device)
