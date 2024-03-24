"""
Login (authorization) endpoint is defined here.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from test_fastapi.logic.users import authorize
from test_fastapi.logic.users import refresh_tokens as refresh
from test_fastapi.schemas.users import LoginResponse

from .router import user_data_router


@user_data_router.post("/login", status_code=status.HTTP_200_OK)
async def authorize_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginResponse:
    """
    Authorizes user by given username and password if user exists and active.

    Return access and refresh tokens, which user would need to store and send
    in `Authorization` header with requests later.

    If the given device value was already set for other token of a given user, then old token is overwrited.
    """

    tokens = await authorize(form_data.username, form_data.password)

    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)


@user_data_router.post("/refresh_tokens", status_code=status.HTTP_200_OK)
async def refresh_tokens(
    refresh_token: str
) -> LoginResponse:
    """
    Return access and refresh tokens for a given refresh token if it is valid and user is active.

    Returns access and refresh tokens, which user would need to store and send
    in `Authorization` header with requests later.

    If the given device value was already set for other token of a given user, then old token is overwrited.
    """

    tokens = await refresh(refresh_token)

    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)